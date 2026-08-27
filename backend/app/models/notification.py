from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime, timezone


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    type = Column(String, default="info")
    # study_reminder | streak_warning | roadmap_update | new_recommendation |
    # job_match | interview_reminder | achievement | info
    title = Column(String, nullable=False)
    body = Column(Text, default="")
    link = Column(String, default="")  # in-app route e.g. /dashboard
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    user = relationship("User", back_populates="notifications")


class Achievement(Base):
    """Achievement definitions (seeded)."""
    __tablename__ = "achievements"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, default="")
    icon = Column(String, default="award")
    xp_reward = Column(Integer, default=50)

    user_achievements = relationship("UserAchievement", back_populates="achievement", cascade="all, delete-orphan")


class UserAchievement(Base):
    __tablename__ = "user_achievements"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    achievement_id = Column(Integer, ForeignKey("achievements.id"), nullable=False)
    earned_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    user = relationship("User", back_populates="achievements")
    achievement = relationship("Achievement", back_populates="user_achievements")


class RoadmapVersion(Base):
    """Version tracking for roadmap content evolution / admin approval."""
    __tablename__ = "roadmap_versions"

    id = Column(Integer, primary_key=True, index=True)
    career_path_id = Column(Integer, ForeignKey("career_paths.id"), nullable=False)
    version = Column(String, nullable=False)  # semver-ish string
    status = Column(String, default="active")  # draft | pending_approval | active | archived
    changelog = Column(Text, default="")
    skill_frequency_snapshot = Column(Text, default="{}")  # JSON: skill -> JD frequency
    emerging_skills = Column(Text, default="[]")  # JSON list
    declining_skills = Column(Text, default="[]")  # JSON list
    published_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    career_path = relationship("CareerPath", back_populates="versions")
