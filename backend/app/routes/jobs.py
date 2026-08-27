from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.job import JobDescription
from app.models.career import CareerPath
from app.models.skill import Skill, SkillAlias, UserSkill
from app.auth import get_current_user
from app.models.user import User
from app.schemas.job import (
    JobAnalyzeRequest, JobAnalysisResponse, JobSummaryResponse,
    GapItemSchema, ParsedMeta, JobCompareItem, JobCompareResponse,
)
from app.services.job_parser import JobParser
from app.services.gap_analyzer import GapAnalyzer, GapReport
from app.services.normalizer import normalize_skill_name, canonical_key
from app.services.gamification import award_xp, XP_RULES
import json


def _build_context(db: Session, user: User):
    """Known skill vocabulary + user state maps for the analyzer."""
    career = None
    if user.selected_career_id:
        career = db.query(CareerPath).filter(CareerPath.id == user.selected_career_id).first()

    # Vocabulary: every skill in DB (any career) so cross-career skills match too
    all_skills = db.query(Skill).all()
    known_names = [s.name for s in all_skills]

    career_skill_map: dict = {}
    if career:
        for s in db.query(Skill).filter(Skill.career_path_id == career.id).all():
            meta = {
                "skill_id": s.id, "name": s.name,
                "priority": s.priority, "hours": s.estimated_hours or 8,
            }
            career_skill_map.setdefault(canonical_key(s.name), meta)
            career_skill_map.setdefault(s.slug.replace("_", "-"), meta)
            for a in s.aliases:
                career_skill_map.setdefault(canonical_key(a.alias), meta)

    user_skill_map: dict = {}
    rows = db.query(UserSkill).filter(UserSkill.user_id == user.id).all()
    id_to_skill = {s.id: s for s in all_skills}
    for r in rows:
        s = id_to_skill.get(r.skill_id)
        if not s:
            continue
        user_skill_map[canonical_key(s.name)] = {
            "status": r.status, "confidence": r.confidence or 0,
            "skill_id": s.id, "name": s.name,
        }

    return known_names, career_skill_map, user_skill_map, career


def _gap_to_schema(g) -> GapItemSchema:
    return GapItemSchema(
        canonical=g.canonical, display_name=g.display_name,
        requirement_type=g.requirement_type, category=g.category,
        user_status=g.user_status, confidence=g.confidence,
        matched_skill_id=g.matched_skill_id, estimated_hours=g.estimated_hours,
        priority_score=g.priority_score, priority_label=g.priority_label,
    )


def analyze_and_persist(
    db: Session,
    user: User,
    request: JobAnalyzeRequest,
) -> JobAnalysisResponse:
    """Full pipeline: parse -> gap analysis -> persist. Business logic lives in services."""
    known_names, career_skill_map, user_skill_map, career = _build_context(db, user)

    parser = JobParser(known_names)
    parsed = parser.parse(request.raw_text)
    parsed = parser.enrich_with_llm(parsed, request.raw_text)

    analyzer = GapAnalyzer()
    report: GapReport = analyzer.analyze(parsed, user_skill_map, career_skill_map)

    job = JobDescription(
        user_id=user.id,
        title=(request.title or "Untitled Position")[:160],
        company=(request.company or "")[:120],
        location=(request.location or "")[:120],
        raw_text=request.raw_text,
        match_score=report.match_score,
        is_saved=1 if request.save else 0,
        parsed_meta=json.dumps({
            "years_experience": parsed.years_experience,
            "education": parsed.education,
            "certifications": parsed.certifications,
            "soft_skills": parsed.soft_skills,
            "domains": parsed.domains,
        }),
    )
    db.add(job)
    db.flush()

    from app.models.job import JobSkill
    seen_canonical = set()
    for bucket, req_default in (
        (report.exact_matches, None),
        (report.partial_matches, None),
        (report.missing_required, None),
        (report.missing_preferred, "preferred"),
    ):
        for g in bucket:
            if g.canonical in seen_canonical:
                continue
            seen_canonical.add(g.canonical)
            db.add(JobSkill(
                job_description_id=job.id,
                skill_name=g.display_name[:160],
                normalized_name=g.canonical[:160],
                matched_skill_id=g.matched_skill_id,
                requirement_type=g.requirement_type if g.requirement_type in ("required", "preferred") else "required",
                frequency=1,
                category=g.category,
            ))

    award_xp(user, XP_RULES["job_analyzed"])
    db.commit()

    return JobAnalysisResponse(
        id=job.id,
        title=job.title,
        company=job.company,
        location=job.location,
        match_score=report.match_score,
        exact_matches=[_gap_to_schema(g) for g in report.exact_matches],
        partial_matches=[_gap_to_schema(g) for g in report.partial_matches],
        missing_required=[_gap_to_schema(g) for g in report.missing_required],
        missing_preferred=[_gap_to_schema(g) for g in report.missing_preferred],
        overqualified=[_gap_to_schema(g) for g in report.overqualified[:8]],
        learn_first=[_gap_to_schema(g) for g in report.learn_first],
        parsed_meta=ParsedMeta(
            years_experience=parsed.years_experience,
            education=parsed.education,
            certifications=parsed.certifications,
            soft_skills=parsed.soft_skills,
            domains=parsed.domains,
        ),
    )


router = APIRouter(prefix="/jobs", tags=["Job Analyzer"])


@router.post("/analyze", response_model=JobAnalysisResponse)
def analyze_job(
    request: JobAnalyzeRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return analyze_and_persist(db, user, request)


@router.get("", response_model=List[JobSummaryResponse])
@router.get("/saved", response_model=List[JobSummaryResponse])
def list_jobs(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    rows = db.query(JobDescription).filter(JobDescription.user_id == user.id)\
        .order_by(JobDescription.created_at.desc()).limit(50).all()
    return [JobSummaryResponse.model_validate(r) for r in rows]


@router.post("/compare", response_model=JobCompareResponse)
def compare_jobs(
    job_ids: List[int],
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if len(job_ids) < 2 or len(job_ids) > 4:
        raise HTTPException(status_code=400, detail="Select 2-4 jobs to compare")
    rows = db.query(JobDescription).filter(
        JobDescription.user_id == user.id, JobDescription.id.in_(job_ids)).all()

    items: List[JobCompareItem] = []
    missing_sets: List[set] = []
    for j in rows:
        skill_states: dict = {}
        missing = set()
        for js in j.job_skills:
            us = None
            if js.matched_skill_id:
                us_row = db.query(UserSkill).filter(
                    UserSkill.user_id == user.id, UserSkill.skill_id == js.matched_skill_id).first()
                us = us_row.status if us_row else None
            state = "exact" if us == "completed" else ("partial" if us == "in_progress" else "missing")
            skill_states[js.normalized_name] = state
            if state == "missing":
                missing.add(js.normalized_name)
        items.append(JobCompareItem(
            job_id=j.id, title=j.title, company=j.company,
            match_score=j.match_score, skills=skill_states,
        ))
        missing_sets.append(missing)

    common_missing = set.intersection(*missing_sets) if missing_sets else set()
    union_missing = set.union(*missing_sets) if missing_sets else set()
    return JobCompareResponse(
        jobs=items,
        common_missing=sorted(common_missing),
        union_missing=sorted(union_missing),
    )


@router.delete("/{job_id}")
def delete_job(job_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    job = db.query(JobDescription).filter(
        JobDescription.user_id == user.id, JobDescription.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    db.delete(job)
    db.commit()
    return {"ok": True}


@router.get("/{job_id}", response_model=JobAnalysisResponse)
def get_job(job_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    job = db.query(JobDescription).filter(
        JobDescription.user_id == user.id, JobDescription.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    meta = json.loads(job.parsed_meta or "{}")
    exact, partial, miss_req, miss_pref, over = [], [], [], [], []

    from app.models.skill import UserSkill as US
    for js in job.job_skills:
        us = None
        conf = 0
        if js.matched_skill_id:
            row = db.query(US).filter(US.user_id == user.id, US.skill_id == js.matched_skill_id).first()
            if row:
                us, conf = row.status, row.confidence or 0
        g = GapItemSchema(
            canonical=js.normalized_name or js.skill_name.lower(),
            display_name=js.skill_name,
            requirement_type=js.requirement_type,
            category=js.category or "technical",
            user_status=us or "not_started",
            confidence=conf,
            matched_skill_id=js.matched_skill_id,
        )
        if us == "completed":
            exact.append(g)
        elif us == "in_progress":
            partial.append(g)
        elif g.requirement_type == "preferred":
            miss_pref.append(g)
        else:
            miss_req.append(g)

    requested = {g.canonical for g in exact + partial + miss_req + miss_pref}
    completed_rows = db.query(US).filter(US.user_id == user.id, US.status == "completed").all()
    id_to_skill = {s.id: s for s in db.query(Skill).filter(Skill.id.in_([r.skill_id for r in completed_rows])).all()} if completed_rows else {}
    for r in completed_rows:
        s = id_to_skill.get(r.skill_id)
        if not s:
            continue
        canon = canonical_key(s.name)
        if canon not in requested:
            over.append(GapItemSchema(canonical=canon, display_name=s.name,
                                      requirement_type="required", user_status="completed",
                                      matched_skill_id=s.id))

    total_req = len(exact) + len(partial) + len(miss_req)
    score = round(len(exact) / total_req * 100, 1) if total_req else 0.0
    ranked = sorted(miss_req + miss_pref, key=lambda g: -g.priority_score)[:10]

    return JobAnalysisResponse(
        id=job.id, title=job.title, company=job.company, location=job.location,
        match_score=score,
        exact_matches=exact, partial_matches=partial,
        missing_required=miss_req, missing_preferred=miss_pref,
        overqualified=over[:8], learn_first=ranked,
        parsed_meta=ParsedMeta(**{k: meta.get(k) for k in ParsedMeta.model_fields}),
        created_at=job.created_at,
    )
