from sqlalchemy import Column, Integer, String, Text, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime, timezone


class LearningResource(Base):
    __tablename__ = "learning_resources"

    id = Column(Integer, primary_key=True, index=True)
    skill_id = Column(Integer, ForeignKey("skills.id"), nullable=False)
    title = Column(String, nullable=False)
    url = Column(String, default="")
    resource_type = Column(String, default="docs")
    # docs | video | course | book | github | practice | tutorial | certification
    platform = Column(String, default="")  # Official Docs, freeCodeCamp, Coursera...
    is_free = Column(Integer, default=1)
    difficulty = Column(String, default="beginner")  # beginner | intermediate | advanced
    estimated_hours = Column(Float, default=0)
    description = Column(Text, default="")
    last_verified = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    skill = relationship("Skill", back_populates="resources")
