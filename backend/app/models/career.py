from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime, timezone


class CareerPath(Base):
    __tablename__ = "career_paths"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, nullable=False)
    slug = Column(String, unique=True, nullable=False)
    description = Column(Text, default="")
    icon = Column(String, default="briefcase")
    color = Column(String, default="#6366f1")
    difficulty = Column(String, default="intermediate")  # beginner-friendly | intermediate | advanced
    estimated_hours = Column(Integer, default=0)
    typical_roles = Column(Text, default="[]")  # JSON list of role titles
    major_technologies = Column(Text, default="[]")  # JSON list of tech names
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    skills = relationship("Skill", back_populates="career_path", cascade="all, delete-orphan")
    roadmap_nodes = relationship("RoadmapNode", back_populates="career_path", cascade="all, delete-orphan")
    roadmap_edges = relationship("RoadmapEdge", back_populates="career_path", cascade="all, delete-orphan")
    projects = relationship("Project", back_populates="career_path", cascade="all, delete-orphan")
    interview_questions = relationship("InterviewQuestion", back_populates="career_path", cascade="all, delete-orphan")
    versions = relationship("RoadmapVersion", back_populates="career_path", cascade="all, delete-orphan")
