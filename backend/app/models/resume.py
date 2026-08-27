from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime, timezone


class ResumeProfile(Base):
    __tablename__ = "resume_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    full_name = Column(String, default="")
    email = Column(String, default="")
    phone = Column(String, default="")
    location = Column(String, default="")
    linkedin_url = Column(String, default="")
    github_url = Column(String, default="")
    portfolio_url = Column(String, default="")
    summary = Column(Text, default="")
    target_career_id = Column(Integer, nullable=True)  # career the resume targets
    target_job_id = Column(Integer, nullable=True)  # saved JobDescription to tailor against
    experience = Column(Text, default="[]")  # JSON list
    education = Column(Text, default="[]")  # JSON list
    certifications = Column(Text, default="[]")  # JSON list
    projects = Column(Text, default="[]")  # JSON list
    achievements = Column(Text, default="[]")  # JSON list
    selected_skill_ids = Column(Text, default="[]")  # JSON list of skill ids to feature
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    user = relationship("User", back_populates="resume_profile")


class ATSScore(Base):
    __tablename__ = "ats_scores"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True, nullable=False)
    score = Column(Integer, nullable=False)
    career_id = Column(Integer, nullable=True)
    source = Column(String, default="scan")  # "scan" | "upload"
    matched_keywords = Column(Text, default="[]")  # JSON list
    missing_keywords = Column(Text, default="[]")  # JSON list
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    user = relationship("User", back_populates="ats_scores")
