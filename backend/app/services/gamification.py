"""Gamification: XP awards, levels, achievements."""
from datetime import datetime, timedelta, timezone
from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.notification import Achievement, UserAchievement
from app.models.user import User

XP_RULES = {
    "skill_completed": 100,
    "study_session_30min": 25,
    "project_completed": 250,
    "mock_interview_completed": 150,
    "job_analyzed": 20,
}

LEVEL_THRESHOLDS = [
    (0, "Novice"), (200, "Apprentice"), (500, "Practitioner"),
    (1000, "Journeyman"), (1800, "Expert"), (3000, "Master"), (5000, "Grandmaster"),
]


def level_for_xp(xp: int) -> dict:
    current_level = 1
    title = LEVEL_THRESHOLDS[0][1]
    next_threshold = None
    for i, (threshold, t) in enumerate(LEVEL_THRESHOLDS):
        if xp >= threshold:
            current_level = i + 1
            title = t
            next_threshold = LEVEL_THRESHOLDS[i + 1][0] if i + 1 < len(LEVEL_THRESHOLDS) else None
        else:
            break
    progress = 0.0
    if next_threshold is not None:
        prev = LEVEL_THRESHOLDS[current_level - 1][0]
        span = max(next_threshold - prev, 1)
        progress = round(min((xp - prev) / span * 100, 100), 1)
    return {
        "level": current_level,
        "title": title,
        "xp": xp,
        "next_level_xp": next_threshold,
        "level_progress": progress,
    }


def award_xp(user: User, amount: int) -> None:
    user.xp = (user.xp or 0) + amount


def compute_streak(db: Session, user_id: int) -> dict:
    """Daily study streak from study sessions (UTC dates)."""
    from app.models.skill import StudySession
    sessions = db.query(StudySession).filter(
        StudySession.user_id == user_id,
        StudySession.duration_minutes > 0,
    ).all()
    days = sorted({s.session_date.date() for s in sessions}, reverse=True)
    if not days:
        return {"current_streak": 0, "longest_streak": 0, "last_active": None}
    today = datetime.now(timezone.utc).date()
    current = 0
    # streak counts back from today or yesterday (grace for timezone)
    if days[0] >= today - timedelta(days=1):
        expected = days[0]
        for d in days:
            if d == expected:
                current += 1
                expected = expected - timedelta(days=1)
            elif d < expected:
                break
    longest = 1
    run = 1
    for i in range(1, len(days)):
        if (days[i - 1] - days[i]).days == 1:
            run += 1
            longest = max(longest, run)
        else:
            run = 1
    return {
        "current_streak": current,
        "longest_streak": max(longest, current),
        "last_active": days[0].isoformat(),
    }


def check_and_award_achievements(db: Session, user: User) -> List[str]:
    """Evaluate achievement conditions; award newly earned ones.
    Returns titles of newly earned achievements."""
    from app.models.skill import SkillStatus, StudySession, UserSkill
    from app.models.project import UserProject

    defs = {a.code: a for a in db.query(Achievement).all()}
    earned_codes = {
        ua.achievement_id for ua in db.query(UserAchievement).filter(
            UserAchievement.user_id == user.id).all()
    }
    newly: List[str] = []

    def award(code: str):
        a = defs.get(code)
        if not a or a.id in earned_codes:
            return
        db.add(UserAchievement(user_id=user.id, achievement_id=a.id))
        award_xp(user, a.xp_reward)
        newly.append(a.title)

    user_skills = db.query(UserSkill).filter(UserSkill.user_id == user.id).all()
    completed = [us for us in user_skills if us.status == SkillStatus.COMPLETED.value]
    total_sessions = db.query(StudySession).filter(StudySession.user_id == user.id).count()
    projects_done = db.query(UserProject).filter(
        UserProject.user_id == user.id,
        UserProject.status == "completed").count()

    if len(completed) >= 1:
        award("first_skill")
    if len(completed) >= 10:
        award("ten_skills")
    if len(completed) >= 25:
        award("twenty_five_skills")
    if total_sessions >= 1:
        award("first_session")
    if total_sessions >= 25:
        award("session_regular")
    if projects_done >= 1:
        award("first_project")
    if projects_done >= 3:
        award("three_projects")

    streak = compute_streak(db, user.id)["current_streak"]
    if streak >= 7:
        award("streak_7")
    if streak >= 30:
        award("streak_30")

    if user.job_descriptions.limit(1).count() >= 1 if hasattr(user.job_descriptions, "limit") else False:
        award("first_job_analysis")

    if newly:
        db.commit()
    return newly
