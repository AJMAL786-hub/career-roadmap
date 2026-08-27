"""Dashboard aggregation service — computes everything the dashboard needs."""
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Optional

from sqlalchemy.orm import Session

from app.models.career import CareerPath
from app.models.job import JobDescription
from app.models.skill import RoadmapEdge, Skill, StudySession, UserSkill
from app.models.user import User
from app.services.gamification import compute_streak, level_for_xp
from app.services.recommender import RecommendationEngine


def _weekly_study(db: Session, user_id: int) -> List[dict]:
    """Minutes studied per day for the last 7 days."""
    today = datetime.now(timezone.utc).date()
    start = datetime(today.year, today.month, today.day, tzinfo=timezone.utc) - timedelta(days=6)
    sessions = db.query(StudySession).filter(
        StudySession.user_id == user_id,
        StudySession.session_date >= start,
    ).all()
    per_day: Dict[str, int] = {}
    for i in range(7):
        d = start.date() + timedelta(days=i)
        per_day[d.isoformat()] = 0
    for s in sessions:
        key = s.session_date.date().isoformat()
        if key in per_day:
            per_day[key] += s.duration_minutes
    return [
        {"date": k, "label": datetime.fromisoformat(k).strftime("%a"), "minutes": v}
        for k, v in per_day.items()
    ]


def get_dashboard(db: Session, user: User) -> dict:
    career: Optional[CareerPath] = None
    if user.selected_career_id:
        career = db.query(CareerPath).filter(CareerPath.id == user.selected_career_id).first()

    completed = in_progress = not_started = 0
    category_progress: Dict[str, float] = {}
    estimated_remaining = 0.0
    recommended_next: List[dict] = []
    top_gaps: List[dict] = []
    job_readiness = 0.0

    user_skills = db.query(UserSkill).filter(UserSkill.user_id == user.id).all()
    status_by_skill = {us.skill_id: us for us in user_skills}

    if career:
        skills = db.query(Skill).filter(Skill.career_path_id == career.id).all()
        edges = db.query(RoadmapEdge).filter(RoadmapEdge.career_path_id == career.id).all()

        cat_totals: Dict[str, int] = {}
        cat_done: Dict[str, int] = {}
        node_list, edge_list, status_map = [], [], {}
        for s in skills:
            us = status_by_skill.get(s.id)
            st = us.status if us else "not_started"
            status_map[s.id] = {"status": st, "confidence": us.confidence if us else 0}
            cat_totals[s.category] = cat_totals.get(s.category, 0) + 1
            if st == "completed":
                completed += 1
                cat_done[s.category] = cat_done.get(s.category, 0) + 1
            elif st == "in_progress":
                in_progress += 1
                progress = us.progress or 0
                estimated_remaining += max(s.estimated_hours * (1 - progress / 100), 0)
            else:
                not_started += 1
                estimated_remaining += s.estimated_hours

            node_list.append({
                "skill_id": s.id, "name": s.name, "priority": s.priority,
                "level": s.level, "hours": s.estimated_hours, "category": s.category,
            })
        for e in edges:
            edge_list.append({"source_skill_id": e.source_skill_id,
                              "target_skill_id": e.target_skill_id})

        for cat, total in cat_totals.items():
            done = cat_done.get(cat, 0)
            category_progress[cat] = round(done / total * 100, 1) if total else 0

        engine = RecommendationEngine(node_list, edge_list, status_map)
        recommended_next = engine.recommend_next(limit=3)

        total_skills = len(skills)
        overall = round(completed / total_skills * 100, 1) if total_skills else 0

        # Job readiness blends roadmap completion with confidence of completed skills
        conf_sum = sum(
            (status_by_skill[s.id].confidence or 3)
            for s in skills if status_by_skill.get(s.id) and status_by_skill[s.id].status == "completed"
        )
        conf_avg = (conf_sum / completed / 5 * 100) if completed else 60
        job_readiness = round(min(overall * 0.75 + conf_avg * 0.25, 100), 1)

        # Top skill gaps from saved jobs (missing required skills by frequency)
        gap_counts: Dict[str, dict] = {}
        jobs = db.query(JobDescription).filter(
            JobDescription.user_id == user.id).order_by(
            JobDescription.created_at.desc()).limit(10).all()
        for j in jobs:
            for js in j.job_skills:
                if js.requirement_type == "required" and js.matched_skill_id is None \
                        and js.normalized_name:
                    entry = gap_counts.setdefault(js.normalized_name, {
                        "skill": js.normalized_name.replace("-", " ").title(),
                        "count": 0})
                    entry["count"] += js.frequency
        top_gaps = sorted(gap_counts.values(), key=lambda g: -g["count"])[:5]

    total_minutes = sum(
        (m[0] or 0) for m in db.query(StudySession.duration_minutes)
        .filter(StudySession.user_id == user.id).all()
    )

    streak_info = compute_streak(db, user.id)

    recent_activity = []
    recent_rows = db.query(UserSkill).filter(
        UserSkill.user_id == user.id).order_by(
        UserSkill.updated_at.desc()).limit(6).all()
    for us in recent_rows:
        skill = db.query(Skill).filter(Skill.id == us.skill_id).first()
        if skill:
            recent_activity.append({
                "type": "skill",
                "name": skill.name,
                "status": us.status,
                "at": us.updated_at.isoformat() if us.updated_at else None,
            })

    recent_sessions = db.query(StudySession).filter(
        StudySession.user_id == user.id).order_by(
        StudySession.session_date.desc()).limit(4).all()
    for s in recent_sessions:
        name = None
        if s.skill_id:
            sk = db.query(Skill).filter(Skill.id == s.skill_id).first()
            name = sk.name if sk else None
        recent_activity.append({
            "type": "study",
            "name": f"{s.duration_minutes} min study" + (f" — {name}" if name else ""),
            "status": "logged",
            "at": s.session_date.isoformat(),
        })
    recent_activity.sort(key=lambda a: a["at"] or "", reverse=True)
    recent_activity = recent_activity[:8]

    latest_jobs = []
    jobs = db.query(JobDescription).filter(
        JobDescription.user_id == user.id).order_by(
        JobDescription.created_at.desc()).limit(4).all()
    for j in jobs:
        latest_jobs.append({
            "id": j.id, "title": j.title, "company": j.company,
            "match_score": j.match_score,
            "created_at": j.created_at.isoformat() if j.created_at else None,
        })

    return {
        "target_career": {"id": career.id, "title": career.title,
                          "slug": career.slug, "color": career.color} if career else None,
        "overall_progress": round(completed / max(completed + in_progress + not_started, 1) * 100, 1),
        "total_skills": completed + in_progress + not_started,
        "completed_skills": completed,
        "in_progress_skills": in_progress,
        "remaining_skills": not_started,
        "estimated_remaining_hours": round(estimated_remaining, 1),
        "category_progress": category_progress,
        "current_streak": streak_info["current_streak"],
        "longest_streak": streak_info["longest_streak"],
        "total_study_minutes": total_minutes,
        "weekly_study": _weekly_study(db, user.id),
        "recommended_next": recommended_next,
        "job_readiness_score": job_readiness,
        "recent_activity": recent_activity,
        "latest_jobs": latest_jobs,
        "top_gaps": top_gaps,
        "gamification": level_for_xp(user.xp or 0),
    }
