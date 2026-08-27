from sqlalchemy import Column, Integer, String, Text, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime, timezone


class JobDescription(Base):
    __tablename__ = "job_descriptions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    company = Column(String, default="")
    location = Column(String, default="")
    raw_text = Column(Text, nullable=False)
    match_score = Column(Float, default=0)
    is_saved = Column(Integer, default=1)
    # Parsed structured metadata (JSON strings)
    parsed_meta = Column(Text, default="{}")
    # {years_experience, education, certifications, soft_skills, domains,
    #  programming_languages, frameworks, tools, cloud, databases}
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    user = relationship("User", back_populates="job_descriptions")
    job_skills = relationship("JobSkill", back_populates="job_description", cascade="all, delete-orphan")


class JobSkill(Base):
    __tablename__ = "job_skills"

    id = Column(Integer, primary_key=True, index=True)
    job_description_id = Column(Integer, ForeignKey("job_descriptions.id"), nullable=False)
    skill_name = Column(String, nullable=False)  # as found in the JD
    normalized_name = Column(String, default="")
    matched_skill_id = Column(Integer, ForeignKey("skills.id"), nullable=True)
    requirement_type = Column(String, default="required")  # required | preferred
    frequency = Column(Integer, default=1)  # mentions in text
    category = Column(String, default="technical")  # inferred bucket
    is_matched = Column(Integer, default=0)

    job_description = relationship("JobDescription", back_populates="job_skills")
    matched_skill = relationship("Skill")
