from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timezone

from app.database import get_db
from app.models.interview import InterviewQuestion, InterviewProgress, MockInterview
from app.models.career import CareerPath
from app.auth import get_current_user
from app.models.user import User
from app.schemas.misc import (
    InterviewQuestionResponse, InterviewProgressUpdate,
    MockInterviewCreate, MockInterviewComplete, MockInterviewResponse,
    InterviewStatsResponse,
)
from app.services.gamification import award_xp, XP_RULES

router = APIRouter(prefix="/interviews", tags=["Interview Prep"])

CATEGORIES = ["programming", "dsa", "databases", "system_design", "ml",
              "cloud", "devops", "cybersecurity", "behavioral"]


def _question_response(db: Session, q: InterviewQuestion, user: User) -> InterviewQuestionResponse:
    prog = db.query(InterviewProgress).filter(
        InterviewProgress.user_id == user.id,
        InterviewProgress.question_id == q.id).first()
    return InterviewQuestionResponse(
        id=q.id, question=q.question, answer=q.answer or "",
        difficulty=q.difficulty, category=q.category, company=q.company or "",
        skill_name=q.skill.name if q.skill else None,
        mastered=bool(prog.mastered) if prog else False,
        times_practiced=prog.times_practiced if prog else 0,
        confidence=prog.confidence if prog else 0,
    )


@router.get("/questions", response_model=List[InterviewQuestionResponse])
def list_questions(
    career_id: Optional[int] = None,
    category: Optional[str] = None,
    difficulty: Optional[str] = None,
    mastered: Optional[bool] = None,
    limit: int = 100,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    career_id = career_id or user.selected_career_id
    query = db.query(InterviewQuestion).options(__import__("sqlalchemy").orm.joinedload(InterviewQuestion.skill))
    if career_id:
        query = query.filter(InterviewQuestion.career_path_id == career_id)
    if category:
        if category not in CATEGORIES:
            raise HTTPException(status_code=400, detail="Invalid category")
        query = query.filter(InterviewQuestion.category == category)
    if difficulty:
        if difficulty not in ("beginner", "intermediate", "advanced"):
            raise HTTPException(status_code=400, detail="Invalid difficulty")
        query = query.filter(InterviewQuestion.difficulty == difficulty)
    rows = query.order_by(InterviewQuestion.id.asc()).limit(min(limit, 300)).all()

    results = [_question_response(db, q, user) for q in rows]
    if mastered is not None:
        results = [r for r in results if r.mastered == mastered]
    return results


@router.put("/questions/{question_id}", response_model=InterviewQuestionResponse)
@router.put("/progress/{question_id}", response_model=InterviewQuestionResponse)
def update_question_progress(
    question_id: int,
    data: InterviewProgressUpdate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    q = db.query(InterviewQuestion).filter(InterviewQuestion.id == question_id).first()
    if not q:
        raise HTTPException(status_code=404, detail="Question not found")

    prog = db.query(InterviewProgress).filter(
        InterviewProgress.user_id == user.id,
        InterviewProgress.question_id == question_id).first()
    if not prog:
        prog = InterviewProgress(user_id=user.id, question_id=question_id)
        db.add(prog)

    if data.mastered is not None:
        was_mastered = prog.mastered
        prog.mastered = data.mastered
        if data.mastered and not was_mastered:
            award_xp(user, 30)
    if data.confidence is not None:
        prog.confidence = data.confidence
    if data.practiced:
        prog.times_practiced = (prog.times_practiced or 0) + 1
        prog.last_practiced_at = datetime.now(timezone.utc)

    db.flush()
    db.commit()
    return _question_response(db, q, user)


@router.get("/stats", response_model=InterviewStatsResponse)
def interview_stats(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    career_id = user.selected_career_id
    base = db.query(InterviewQuestion)
    total_q = base.filter(InterviewQuestion.career_path_id == career_id).count() if career_id else 0

    by_category: dict = {}
    if career_id:
        questions = db.query(InterviewQuestion).filter(
            InterviewQuestion.career_path_id == career_id).all()
        prog_rows = {p.question_id: p for p in db.query(InterviewProgress).filter(
            InterviewProgress.user_id == user.id).all()}
        for q in questions:
            entry = by_category.setdefault(q.category, {"total": 0, "mastered": 0})
            entry["total"] += 1
            p = prog_rows.get(q.id)
            if p and p.mastered:
                entry["mastered"] += 1

    mocks = db.query(MockInterview).filter(MockInterview.user_id == user.id)\
        .order_by(MockInterview.created_at.desc()).limit(20).all()

    mastered_total = sum(v["mastered"] for v in by_category.values())
    return InterviewStatsResponse(
        total_questions=total_q,
        mastered_questions=mastered_total,
        by_category=by_category,
        mock_interviews=[MockInterviewResponse.model_validate(m) for m in mocks],
    )


@router.post("/mocks", response_model=MockInterviewResponse)
@router.post("/mock", response_model=MockInterviewResponse)
def schedule_mock(
    data: MockInterviewCreate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    mock = MockInterview(
        user_id=user.id, title=data.title[:160], category=data.category,
        scheduled_for=data.scheduled_for,
    )
    db.add(mock)
    db.commit()
    db.refresh(mock)
    return MockInterviewResponse.model_validate(mock)


@router.put("/mocks/{mock_id}/complete", response_model=MockInterviewResponse)
def complete_mock(
    mock_id: int,
    data: MockInterviewComplete,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    mock = db.query(MockInterview).filter(
        MockInterview.user_id == user.id, MockInterview.id == mock_id).first()
    if not mock:
        raise HTTPException(status_code=404, detail="Mock interview not found")
    mock.completed_at = datetime.now(timezone.utc)
    mock.score = data.score
    mock.notes = (data.notes or "")[:4000]
    award_xp(user, XP_RULES["mock_interview_completed"])
    db.commit()
    db.refresh(mock)
    return MockInterviewResponse.model_validate(mock)


@router.delete("/mocks/{mock_id}")
def delete_mock(mock_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    mock = db.query(MockInterview).filter(
        MockInterview.user_id == user.id, MockInterview.id == mock_id).first()
    if not mock:
        raise HTTPException(status_code=404, detail="Mock interview not found")
    db.delete(mock)
    db.commit()
    return {"ok": True}
