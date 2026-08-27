from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timezone

from app.database import get_db
from app.models.skill import (
    Skill, SkillAlias, UserSkill, RoadmapEdge, Evidence,
    SkillStatus,
)
from app.models.learning import LearningResource
from app.models.notification import Notification
from app.auth import get_current_user, get_optional_user
from app.models.user import User
from app.schemas.career import (
    SkillDetailResponse, SkillCreateRequest, SkillProgressUpdate,
    UserSkillResponse, SkillAliasResponse, ResourceResponse, EvidenceCreate,
    EvidenceResponse,
)
from app.services.gamification import award_xp, XP_RULES, check_and_award_achievements

router = APIRouter(prefix="/skills", tags=["Skills"])

ALLOWED_URL_SCHEMES = ("http://", "https://")


def _validate_url(url: str, field: str = "url") -> str:
    if url and not url.startswith(ALLOWED_URL_SCHEMES):
        raise HTTPException(status_code=400, detail=f"{field} must be a valid http(s) URL")
    return (url or "")[:500]


@router.get("/user/all", response_model=List[UserSkillResponse])
def get_user_skills(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    rows = db.query(UserSkill).filter(UserSkill.user_id == user.id).all()
    return [UserSkillResponse.model_validate(r) for r in rows]


@router.get("/{skill_id}", response_model=SkillDetailResponse)
def get_skill_detail(
    skill_id: int,
    user: User = Depends(get_optional_user),
    db: Session = Depends(get_db),
):
    skill = db.query(Skill).filter(Skill.id == skill_id).first()
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")

    aliases = db.query(SkillAlias).filter(SkillAlias.skill_id == skill_id).all()
    prereq_edges = db.query(RoadmapEdge).filter(RoadmapEdge.target_skill_id == skill_id).all()
    dependent_edges = db.query(RoadmapEdge).filter(RoadmapEdge.source_skill_id == skill_id).all()

    prereq_ids = [e.source_skill_id for e in prereq_edges]
    dependent_ids = [e.target_skill_id for e in dependent_edges]

    related_ids = prereq_ids + dependent_ids
    related_skills = {s.id: s for s in db.query(Skill).filter(Skill.id.in_(related_ids)).all()} if related_ids else {}

    # user states for prereqs + this skill
    user_states = {}
    if user and related_ids + [skill_id]:
        ids = list(set(related_ids + [skill_id]))
        rows = db.query(UserSkill).filter(
            UserSkill.user_id == user.id, UserSkill.skill_id.in_(ids)).all()
        user_states = {r.skill_id: r for r in rows}

    def _state_dict(sid):
        s = related_skills.get(sid)
        if not s:
            return {"skill_id": sid, "name": "?", "status": "not_started"}
        us = user_states.get(sid)
        return {
            "skill_id": sid, "name": s.name,
            "status": us.status if us else "not_started",
            "category": s.category,
        }

    resources = db.query(LearningResource).filter(
        LearningResource.skill_id == skill_id).all()
    resource_list = [
        ResourceResponse(
            id=r.id, title=r.title, url=r.url, resource_type=r.resource_type,
            platform=r.platform, is_free=bool(r.is_free), difficulty=r.difficulty,
            estimated_hours=r.estimated_hours or 0, description=r.description or "",
        ) for r in resources
    ]

    us = user_states.get(skill_id)
    user_state = {}
    if us:
        user_state = {
            "status": us.status, "progress": us.progress,
            "confidence": us.confidence or 0, "notes": us.notes or "",
            "certificate_name": us.certificate_name or "",
            "github_url": us.github_url or "",
            "started_at": us.started_at.isoformat() if us.started_at else None,
            "completed_at": us.completed_at.isoformat() if us.completed_at else None,
        }

    return SkillDetailResponse(
        id=skill.id, career_path_id=skill.career_path_id, name=skill.name,
        slug=skill.slug, description=skill.description or "",
        why_important=skill.why_important or "", level=skill.level,
        category=skill.category, priority=skill.priority,
        estimated_hours=skill.estimated_hours, is_custom=skill.is_custom or 0,
        aliases=[SkillAliasResponse(id=a.id, alias=a.alias) for a in aliases],
        prerequisites=[_state_dict(i) for i in prereq_ids],
        dependents=[_state_dict(i) for i in dependent_ids],
        resources=resource_list,
        user_state=user_state,
    )


@router.post("/custom", response_model=SkillDetailResponse)
def create_custom_skill(
    data: SkillCreateRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    import re as _re
    if not user.selected_career_id:
        raise HTTPException(status_code=400, detail="Select a career path first")
    career_id = data.career_path_id or user.selected_career_id

    slug = _re.sub(r"[^a-z0-9]+", "-", data.name.lower()).strip("-")[:80]
    base_slug, suffix = slug, 2
    while db.query(Skill).filter(Skill.slug == slug, Skill.career_path_id == career_id).first():
        slug = f"{base_slug}-{suffix}"
        suffix += 1

    skill = Skill(
        career_path_id=career_id, name=data.name.strip()[:80], slug=slug,
        description=(data.description or "")[:2000], why_important=data.why_important or "",
        level=data.level, category=data.category, priority=data.priority,
        estimated_hours=data.estimated_hours, is_custom=1,
    )
    db.add(skill)
    db.flush()

    # place node in the last layer + 1 so it sits at the frontier of the DAG
    max_layer_row = db.query(RoadmapEdge).filter(RoadmapEdge.career_path_id == career_id).first()
    from app.models.skill import RoadmapNode
    top_layer = db.query(RoadmapNode.layer).filter(RoadmapNode.career_path_id == career_id).order_by(RoadmapNode.layer.desc()).first()
    layer = (top_layer[0] + 1) if top_layer else 0
    count_in_layer = db.query(RoadmapNode).filter(RoadmapNode.career_path_id == career_id, RoadmapNode.layer == layer).count()
    db.add(RoadmapNode(
        career_path_id=career_id, skill_id=skill.id, layer=layer,
        position_x=float(layer) * 260.0,
        position_y=float(count_in_layer) * 110.0,
    ))

    valid_prereqs = []
    for pid in data.prerequisites[:10]:
        p = db.query(Skill).filter(Skill.id == pid, Skill.career_path_id == career_id).first()
        if p and p.id != skill.id:
            valid_prereqs.append(p.id)
            db.add(RoadmapEdge(career_path_id=career_id, source_skill_id=p.id, target_skill_id=skill.id))

    db.commit()
    db.refresh(skill)

    return SkillDetailResponse(
        id=skill.id, career_path_id=skill.career_path_id, name=skill.name,
        slug=skill.slug, description=skill.description or "", why_important="",
        level=skill.level, category=skill.category, priority=skill.priority,
        estimated_hours=skill.estimated_hours, is_custom=1,
        aliases=[], resources=[],
        prerequisites=[{"skill_id": pid, "name": "", "status": "completed"} for pid in valid_prereqs],
        dependents=[], user_state={"status": "not_started", "progress": 0},
    )


@router.put("/{skill_id}/progress", response_model=UserSkillResponse)
def update_progress(
    skill_id: int,
    data: SkillProgressUpdate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    skill = db.query(Skill).filter(Skill.id == skill_id).first()
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")

    user_skill = db.query(UserSkill).filter(
        UserSkill.user_id == user.id, UserSkill.skill_id == skill_id).first()
    now = datetime.now(timezone.utc)

    newly_completed = False
    if not user_skill:
        user_skill = UserSkill(user_id=user.id, skill_id=skill_id)
        db.add(user_skill)

    prev_status = user_skill.status
    user_skill.status = data.status
    if data.notes is not None:
        user_skill.notes = data.notes[:4000]
    if data.confidence is not None:
        user_skill.confidence = data.confidence
    if data.certificate_name is not None:
        user_skill.certificate_name = data.certificate_name[:160]
    if data.github_url is not None:
        user_skill.github_url = _validate_url(data.github_url, "github_url")
    if data.status == SkillStatus.IN_PROGRESS.value:
        user_skill.progress = max(data.progress, 5)
        if not user_skill.started_at:
            user_skill.started_at = now
        if user_skill.status != SkillStatus.COMPLETED.value:
            user_skill.completed_at = None
    elif data.status == SkillStatus.COMPLETED.value:
        user_skill.progress = 100
        if not user_skill.completed_at:
            user_skill.completed_at = now
            newly_completed = prev_status != SkillStatus.COMPLETED.value
    else:
        user_skill.progress = 0
        user_skill.started_at = None
        user_skill.completed_at = None

    db.flush()

    if newly_completed:
        award_xp(user, XP_RULES["skill_completed"])
        db.add(Notification(
            user_id=user.id, type="achievement", title=f"Skill completed: {skill.name}",
            body=f"+{XP_RULES['skill_completed']} XP — great progress on your roadmap!",
            link="/roadmap",
        ))

    db.commit()
    db.refresh(user_skill)
    check_and_award_achievements(db, user)
    return UserSkillResponse.model_validate(user_skill)


@router.post("/{skill_id}/evidence", response_model=EvidenceResponse)
def add_evidence(
    skill_id: int,
    data: EvidenceCreate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user_skill = db.query(UserSkill).filter(
        UserSkill.user_id == user.id, UserSkill.skill_id == skill_id).first()
    if not user_skill:
        user_skill = UserSkill(user_id=user.id, skill_id=skill_id, status="in_progress",
                               started_at=datetime.now(timezone.utc))
        db.add(user_skill)
        db.flush()
    evidence = Evidence(
        user_skill_id=user_skill.id,
        title=data.title.strip()[:160],
        description=(data.description or "")[:2000],
        url=_validate_url(data.url),
        evidence_type=data.evidence_type,
    )
    db.add(evidence)
    db.commit()
    db.refresh(evidence)
    return EvidenceResponse.model_validate(evidence)


@router.get("/{skill_id}/evidence", response_model=List[EvidenceResponse])
def list_evidence(
    skill_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user_skill = db.query(UserSkill).filter(
        UserSkill.user_id == user.id, UserSkill.skill_id == skill_id).first()
    if not user_skill:
        return []
    rows = db.query(Evidence).filter(Evidence.user_skill_id == user_skill.id)\
        .order_by(Evidence.created_at.desc()).all()
    return [EvidenceResponse.model_validate(r) for r in rows]
