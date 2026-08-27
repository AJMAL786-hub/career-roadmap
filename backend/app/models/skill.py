from sqlalchemy import Column, Integer, String, Text, Float, DateTime, ForeignKey, Enum as SAEnum
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime, timezone
import enum


class SkillLevel(str, enum.Enum):
    FUNDAMENTAL = "fundamental"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    OPTIONAL = "optional"


class SkillCategory(str, enum.Enum):
    TECHNICAL = "technical"
    SOFT_SKILL = "soft_skill"
    TOOL = "tool"
    FRAMEWORK = "framework"
    CERTIFICATION = "certification"
    DOMAIN = "domain"


class SkillPriority(str, enum.Enum):
    MUST_HAVE = "must_have"
    RECOMMENDED = "recommended"
    OPTIONAL = "optional"


class SkillStatus(str, enum.Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class Skill(Base):
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, index=True)
    career_path_id = Column(Integer, ForeignKey("career_paths.id"), nullable=False)
    name = Column(String, nullable=False)
    slug = Column(String, nullable=False)
    description = Column(Text, default="")
    why_important = Column(Text, default="")
    level = Column(String, default=SkillLevel.FUNDAMENTAL.value)
    category = Column(String, default=SkillCategory.TECHNICAL.value)
    priority = Column(String, default=SkillPriority.RECOMMENDED.value)
    estimated_hours = Column(Float, default=10)
    is_custom = Column(Integer, default=0)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    career_path = relationship("CareerPath", back_populates="skills")
    aliases = relationship("SkillAlias", back_populates="skill", cascade="all, delete-orphan")
    user_skills = relationship("UserSkill", back_populates="skill", cascade="all, delete-orphan")
    resources = relationship("LearningResource", back_populates="skill", cascade="all, delete-orphan")


class SkillAlias(Base):
    __tablename__ = "skill_aliases"

    id = Column(Integer, primary_key=True, index=True)
    skill_id = Column(Integer, ForeignKey("skills.id"), nullable=False)
    alias = Column(String, nullable=False)

    skill = relationship("Skill", back_populates="aliases")


class RoadmapNode(Base):
    __tablename__ = "roadmap_nodes"

    id = Column(Integer, primary_key=True, index=True)
    career_path_id = Column(Integer, ForeignKey("career_paths.id"), nullable=False)
    skill_id = Column(Integer, ForeignKey("skills.id"), nullable=False)
    position_x = Column(Float, default=0)
    position_y = Column(Float, default=0)
    layer = Column(Integer, default=0)

    career_path = relationship("CareerPath", back_populates="roadmap_nodes")
    skill = relationship("Skill")


class RoadmapEdge(Base):
    __tablename__ = "roadmap_edges"

    id = Column(Integer, primary_key=True, index=True)
    career_path_id = Column(Integer, ForeignKey("career_paths.id"), nullable=False)
    source_skill_id = Column(Integer, ForeignKey("skills.id"), nullable=False)
    target_skill_id = Column(Integer, ForeignKey("skills.id"), nullable=False)

    career_path = relationship("CareerPath", back_populates="roadmap_edges")
    source_skill = relationship("Skill", foreign_keys=[source_skill_id])
    target_skill = relationship("Skill", foreign_keys=[target_skill_id])


class UserSkill(Base):
    __tablename__ = "user_skills"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    skill_id = Column(Integer, ForeignKey("skills.id"), nullable=False)
    status = Column(String, default=SkillStatus.NOT_STARTED.value)
    progress = Column(Integer, default=0)
    confidence = Column(Integer, default=0)  # 1-5 self rating
    certificate_name = Column(String, default="")
    github_url = Column(String, default="")
    notes = Column(Text, default="")
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    user = relationship("User", back_populates="skills")
    skill = relationship("Skill", back_populates="user_skills")
    evidence = relationship("Evidence", back_populates="user_skill", cascade="all, delete-orphan")


class Evidence(Base):
    __tablename__ = "evidence"

    id = Column(Integer, primary_key=True, index=True)
    user_skill_id = Column(Integer, ForeignKey("user_skills.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, default="")
    url = Column(String, default="")
    evidence_type = Column(String, default="link")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    user_skill = relationship("UserSkill", back_populates="evidence")


class StudySession(Base):
    __tablename__ = "study_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    skill_id = Column(Integer, ForeignKey("skills.id"), nullable=True)
    duration_minutes = Column(Integer, default=0)
    notes = Column(Text, default="")
    session_date = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    user = relationship("User", back_populates="study_sessions")
    skill = relationship("Skill")
