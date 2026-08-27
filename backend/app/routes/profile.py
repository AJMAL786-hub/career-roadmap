from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.auth import get_current_user
from app.models.user import User
from app.models.notification import Achievement, UserAchievement
from app.schemas.user import ProfileStatsResponse, UserResponse
from app.services.gamification import compute_streak, level_for_xp

router = APIRouter(prefix="/profile", tags=["Profile"])


@router.get("", response_model=ProfileStatsResponse)
def get_profile(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    earned_rows = db.query(UserAchievement).filter(UserAchievement.user_id == user.id).all()
    all_achievements = db.query(Achievement).all()
    earned_ids = {ua.achievement_id for ua in earned_rows}
    achievements = []
    for a in all_achievements:
        ua = next((r for r in earned_rows if r.achievement_id == a.id), None)
        achievements.append({
            "code": a.code, "title": a.title, "description": a.description,
            "icon": a.icon, "earned": a.id in earned_ids,
            "earned_at": ua.earned_at.isoformat() if ua else None,
        })
    return ProfileStatsResponse(
        user=UserResponse.model_validate(user),
        gamification=level_for_xp(user.xp or 0),
        achievements=achievements,
        streak=compute_streak(db, user.id),
    )
