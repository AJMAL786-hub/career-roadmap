from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
import json
from datetime import datetime, timezone

from app.database import get_db
from app.models.project import Project, UserProject, ProjectSkill
from app.auth import get_current_user
from app.models.user import User
from app.schemas.misc import (
    ProjectResponse, UserProjectCreate, UserProjectUpdate, UserProjectResponse,
)
from app.services.gamification import award_xp, XP_RULES, check_and_award_achievements

router = APIRouter(prefix="/projects", tags=["Portfolio Projects"])


def _project_response(db: Session, p: Project, user: Optional[User]) -> ProjectResponse:
    skills = [
        {"id": ps.skill.id, "name": ps.skill.name}
        for ps in p.project_skills if ps.skill
    ]
    user_progress = None
    if user:
        up = db.query(UserProject).filter(
            UserProject.user_id == user.id, UserProject.project_id == p.id).first()
        if up:
            user_progress = UserProjectResponse.model_validate(up)
    return ProjectResponse(
        id=p.id, career_path_id=p.career_path_id, title=p.title, slug=p.slug,
        description=p.description or "", difficulty=p.difficulty,
        estimated_hours=p.estimated_hours or 20,
        technologies=json.loads(p.technologies or "[]"),
        milestones=json.loads(p.milestones or "[]"),
        deliverables=json.loads(p.deliverables or "[]"),
        rubric=json.loads(p.rubric or "[]"),
        skills_demonstrated=skills,
        user_progress=user_progress,
    )


@router.get("", response_model=List[ProjectResponse])
def list_projects(
    career_id: Optional[int] = None,
    difficulty: Optional[str] = None,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    query = db.query(Project).options(joinedload(Project.project_skills).joinedload(ProjectSkill.skill))
    if career_id:
        query = query.filter(Project.career_path_id == career_id)
    if difficulty:
        if difficulty not in ("beginner", "intermediate", "advanced"):
            raise HTTPException(status_code=400, detail="Invalid difficulty filter")
        query = query.filter(Project.difficulty == difficulty)
    rows = query.order_by(Project.id.asc()).all()
    return [_project_response(db, r, user) for r in rows]


@router.get("/{project_id}", response_model=ProjectResponse)
def get_project(
    project_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    p = db.query(Project).filter(Project.id == project_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Project not found")
    return _project_response(db, p, user)


@router.post("/{project_id}/progress", response_model=UserProjectResponse)
@router.post("/{project_id}/start", response_model=UserProjectResponse)
def start_project(
    project_id: int,
    data: Optional[UserProjectCreate] = None,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    existing = db.query(UserProject).filter(
        UserProject.user_id == user.id, UserProject.project_id == project_id).first()
    if existing:
        return UserProjectResponse.model_validate(existing)

    status = data.status if data else "in_progress"
    repo = _safe_url((data.repo_url or data.github_url or "") if data else "")
    live = _safe_url(data.live_url if data else "")
    notes = (data.notes or "")[:4000] if data else ""
    milestones = data.completed_milestones[:50] if data else []

    up = UserProject(
        user_id=user.id, project_id=project_id,
        status=status,
        repo_url=repo,
        live_url=live,
        notes=notes,
        completed_milestones=json.dumps(milestones),
        started_at=datetime.now(timezone.utc) if status != "planned" else None,
        completed_at=datetime.now(timezone.utc) if status == "completed" else None,
        progress=100 if status == "completed" else (10 if status == "in_progress" else 0),
    )
    db.add(up)
    db.commit()
    db.refresh(up)
    return UserProjectResponse.model_validate(up)


@router.put("/{project_id}/progress", response_model=UserProjectResponse)
def update_progress(
    project_id: int,
    data: UserProjectUpdate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    up = db.query(UserProject).filter(
        UserProject.user_id == user.id, UserProject.project_id == project_id).first()
    if not up:
        up = UserProject(
            user_id=user.id, project_id=project_id,
            status=data.status or "in_progress",
            repo_url=_safe_url(data.repo_url or data.github_url or ""),
            live_url=_safe_url(data.live_url or ""),
            notes=(data.notes or "")[:4000],
            completed_milestones=json.dumps(data.completed_milestones or []),
            started_at=datetime.now(timezone.utc),
            progress=100 if data.status == "completed" else (data.progress or 10),
        )
        db.add(up)
        db.flush()

    total_milestones = len(json.loads(project.milestones or "[]")) if project else 0

    newly_completed = False
    if data.status is not None:
        prev = up.status
        up.status = data.status
        if data.status in ("in_progress", "completed") and not up.started_at:
            up.started_at = datetime.now(timezone.utc)
        if data.status == "completed":
            if not up.completed_at:
                up.completed_at = datetime.now(timezone.utc)
                newly_completed = prev != "completed"
            up.progress = 100
    if data.progress is not None and up.status != "completed":
        up.progress = data.progress
    if data.repo_url is not None or data.github_url is not None:
        up.repo_url = _safe_url(data.repo_url or data.github_url)
    if data.live_url is not None:
        up.live_url = _safe_url(data.live_url)
    if data.notes is not None:
        up.notes = data.notes[:4000]
    if data.completed_milestones is not None:
        clean = [i for i in data.completed_milestones if isinstance(i, int) and 0 <= i < max(total_milestones, 1)]
        up.completed_milestones = json.dumps(clean)
        if total_milestones:
            ratio = round(len(clean) / total_milestones * 100)
            up.progress = max(up.progress if up.status != "completed" else 100, min(ratio, 99)) \
                if up.status != "completed" else 100
            if len(clean) == total_milestones and up.status != "completed":
                up.status = "in_progress"

    db.commit()
    db.refresh(up)
    if newly_completed:
        award_xp(user, XP_RULES["project_completed"])
        check_and_award_achievements(db, user)
    return UserProjectResponse.model_validate(up)


def _safe_url(url: str) -> str:
    url = (url or "").strip()
    if url and not url.startswith(("http://", "https://")):
        raise HTTPException(status_code=400, detail="URLs must start with http(s)://")
    return url[:500]
