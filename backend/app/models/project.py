from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime, timezone


class Project(Base):
    """Portfolio project template mapped to roadmap skills."""
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    career_path_id = Column(Integer, ForeignKey("career_paths.id"), nullable=False)
    title = Column(String, nullable=False)
    slug = Column(String, nullable=False)
    description = Column(Text, default="")
    difficulty = Column(String, default="beginner")  # beginner | intermediate | advanced
    estimated_hours = Column(Integer, default=20)
    technologies = Column(Text, default="[]")  # JSON list of strings
    milestones = Column(Text, default="[]")  # JSON list of {title, description}
    deliverables = Column(Text, default="[]")  # JSON list of strings
    rubric = Column(Text, default="[]")  # JSON list of {criterion, weight}
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    career_path = relationship("CareerPath")
    project_skills = relationship("ProjectSkill", back_populates="project", cascade="all, delete-orphan")
    user_projects = relationship("UserProject", back_populates="project", cascade="all, delete-orphan")


class ProjectSkill(Base):
    __tablename__ = "project_skills"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    skill_id = Column(Integer, ForeignKey("skills.id"), nullable=False)

    project = relationship("Project", back_populates="project_skills")
    skill = relationship("Skill")


class UserProject(Base):
    """A user's tracked progress on a portfolio project."""
    __tablename__ = "user_projects"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    status = Column(String, default="planned")  # planned | in_progress | completed
    progress = Column(Integer, default=0)  # 0-100
    repo_url = Column(String, default="")
    live_url = Column(String, default="")
    notes = Column(Text, default="")
    completed_milestones = Column(Text, default="[]")  # JSON list of milestone indexes
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    user = relationship("User", back_populates="projects")
    project = relationship("Project", back_populates="user_projects")
