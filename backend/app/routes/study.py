from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timezone

from app.database import get_db
from app.auth import get_current_user
from app.models.user import User
from app.models.skill import StudySession, Skill
from app.schemas.career import StudySessionCreate, StudySessionResponse
from app.services.gamification import award_xp, XP_RULES, compute_streak, check_and_award_achievements

router = APIRouter(prefix="/study-sessions", tags=["Study Sessions"])


@router.post("", response_model=StudySessionResponse)
def log_session(
    data: StudySessionCreate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if data.skill_id:
        skill = db.query(Skill).filter(Skill.id == data.skill_id).first()
        if not skill:
            raise HTTPException(status_code=404, detail="Skill not found")

    session_date = data.session_date or datetime.now(timezone.utc)
    session = StudySession(
        user_id=user.id,
        skill_id=data.skill_id,
        duration_minutes=data.duration_minutes,
        notes=(data.notes or "")[:2000],
        session_date=session_date,
    )
    db.add(session)
    award_xp(user, XP_RULES["study_session_30min"] * max(1, data.duration_minutes // 30))
    db.commit()
    db.refresh(session)
    check_and_award_achievements(db, user)
    return StudySessionResponse.model_validate(session)


@router.get("", response_model=list[StudySessionResponse])
def list_sessions(
    limit: int = 50,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    rows = (
        db.query(StudySession)
        .filter(StudySession.user_id == user.id)
        .order_by(StudySession.session_date.desc())
        .limit(min(limit, 200))
        .all()
    )
    return [StudySessionResponse.model_validate(r) for r in rows]


@router.get("/stats")
def study_stats(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    from app.services.dashboard import _weekly_study
    total = sum(
        (m[0] or 0) for m in db.query(StudySession.duration_minutes)
        .filter(StudySession.user_id == user.id).all()
    )
    streak = compute_streak(db, user.id)
    return {
        "total_minutes": total,
        "current_streak": streak["current_streak"],
        "longest_streak": streak["longest_streak"],
        "streak": streak,
        "weekly": _weekly_study(db, user.id),
    }
