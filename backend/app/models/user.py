from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime, timezone


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, default="")
    avatar_url = Column(String, default="")
    auth_provider = Column(String, default="local")  # local | google | github (future OAuth)
    provider_id = Column(String, default="")  # OAuth subject id when linked later
    selected_career_id = Column(Integer, nullable=True)
    onboarding_completed = Column(Boolean, default=False)
    xp = Column(Integer, default=0)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    skills = relationship("UserSkill", back_populates="user", cascade="all, delete-orphan")
    study_sessions = relationship("StudySession", back_populates="user", cascade="all, delete-orphan")
    job_descriptions = relationship("JobDescription", back_populates="user", cascade="all, delete-orphan")
    resume_profile = relationship("ResumeProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    ats_scores = relationship("ATSScore", back_populates="user", cascade="all, delete-orphan")
    projects = relationship("UserProject", back_populates="user", cascade="all, delete-orphan")
    interview_progress = relationship("InterviewProgress", back_populates="user", cascade="all, delete-orphan")
    mock_interviews = relationship("MockInterview", back_populates="user", cascade="all, delete-orphan")
    notifications = relationship("Notification", back_populates="user", cascade="all, delete-orphan")
    achievements = relationship("UserAchievement", back_populates="user", cascade="all, delete-orphan")
