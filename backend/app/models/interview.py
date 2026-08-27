from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime, timezone


class InterviewQuestion(Base):
    __tablename__ = "interview_questions"

    id = Column(Integer, primary_key=True, index=True)
    career_path_id = Column(Integer, ForeignKey("career_paths.id"), nullable=False)
    skill_id = Column(Integer, ForeignKey("skills.id"), nullable=True)
    question = Column(Text, nullable=False)
    answer = Column(Text, default="")
    difficulty = Column(String, default="intermediate")  # beginner | intermediate | advanced
    category = Column(String, default="programming")
    # programming | dsa | databases | system_design | ml | cloud | devops |
    # cybersecurity | behavioral
    company = Column(String, default="")  # optional company-specific tag
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    career_path = relationship("CareerPath")
    skill = relationship("Skill")
    progress = relationship("InterviewProgress", back_populates="question", cascade="all, delete-orphan")


class InterviewProgress(Base):
    """Per-user mastery state for an interview question."""
    __tablename__ = "interview_progress"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    question_id = Column(Integer, ForeignKey("interview_questions.id"), nullable=False)
    mastered = Column(Boolean, default=False)
    times_practiced = Column(Integer, default=0)
    confidence = Column(Integer, default=0)  # 0-5 self rating
    last_practiced_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    user = relationship("User", back_populates="interview_progress")
    question = relationship("InterviewQuestion", back_populates="progress")


class MockInterview(Base):
    """Tracker for scheduled/completed mock interview sessions."""
    __tablename__ = "mock_interviews"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    category = Column(String, default="mixed")
    scheduled_for = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    score = Column(Integer, nullable=True)  # 0-100 self assessment
    notes = Column(Text, default="")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    user = relationship("User", back_populates="mock_interviews")
