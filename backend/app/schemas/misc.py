import json
from pydantic import BaseModel, Field, field_validator
from typing import Optional, List, Dict, Any
from datetime import datetime


# ----------------------------------------------------------------- projects
class MilestoneSchema(BaseModel):
    title: str
    description: str = ""


class RubricSchema(BaseModel):
    criterion: str
    weight: int = 20


class ProjectResponse(BaseModel):
    id: int
    career_path_id: int
    title: str
    slug: str
    description: str = ""
    difficulty: str = "beginner"
    estimated_hours: int = 20
    technologies: List[str] = []
    milestones: List[MilestoneSchema] = []
    deliverables: List[str] = []
    rubric: List[RubricSchema] = []
    skills_demonstrated: List[Dict[str, Any]] = []  # [{id, name}]
    user_progress: Optional["UserProjectResponse"] = None

    class Config:
        from_attributes = True


class UserProjectCreate(BaseModel):
    status: str = Field(default="planned", pattern="^(planned|in_progress|completed)$")
    repo_url: str = ""
    github_url: Optional[str] = None
    live_url: str = ""
    notes: str = ""
    completed_milestones: List[int] = []


class UserProjectUpdate(BaseModel):
    status: Optional[str] = Field(default=None, pattern="^(planned|in_progress|completed)$")
    progress: Optional[int] = Field(default=None, ge=0, le=100)
    repo_url: Optional[str] = None
    github_url: Optional[str] = None
    live_url: Optional[str] = None
    notes: Optional[str] = None
    completed_milestones: Optional[List[int]] = None


class UserProjectResponse(BaseModel):
    id: int
    project_id: int
    status: str
    progress: int
    repo_url: str = ""
    live_url: str = ""
    notes: str = ""
    completed_milestones: List[int] = []
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    @field_validator("completed_milestones", mode="before")
    @classmethod
    def _parse_json_column(cls, v):
        if isinstance(v, str):
            try:
                return json.loads(v)
            except (ValueError, TypeError):
                return []
        return v or []

    class Config:
        from_attributes = True


# ----------------------------------------------------------------- interviews
class InterviewQuestionResponse(BaseModel):
    id: int
    question: str
    answer: str = ""
    difficulty: str = "intermediate"
    category: str = "programming"
    company: str = ""
    skill_name: Optional[str] = None
    mastered: bool = False
    times_practiced: int = 0
    confidence: int = 0

    class Config:
        from_attributes = True


class InterviewProgressUpdate(BaseModel):
    mastered: Optional[bool] = None
    confidence: Optional[int] = Field(default=None, ge=0, le=5)
    practiced: bool = False


class MockInterviewCreate(BaseModel):
    title: str = Field(min_length=1, max_length=160)
    category: str = "mixed"
    scheduled_for: Optional[datetime] = None


class MockInterviewComplete(BaseModel):
    score: int = Field(ge=0, le=100)
    notes: str = ""


class MockInterviewResponse(BaseModel):
    id: int
    title: str
    category: str
    scheduled_for: Optional[datetime]
    completed_at: Optional[datetime]
    score: Optional[int]
    notes: str = ""

    class Config:
        from_attributes = True


class InterviewStatsResponse(BaseModel):
    total_questions: int
    mastered_questions: int
    by_category: Dict[str, Dict[str, int]] = {}
    mock_interviews: List[MockInterviewResponse] = []


# ----------------------------------------------------------------- resume
class ExperienceItem(BaseModel):
    role: str = ""
    company: str = ""
    start: str = ""
    end: str = ""
    bullets: List[str] = []


class EducationItem(BaseModel):
    degree: str = ""
    institution: str = ""
    start: str = ""
    end: str = ""
    details: str = ""


class CertificationItem(BaseModel):
    name: str = ""
    issuer: str = ""
    year: str = ""


class ResumeProjectItem(BaseModel):
    name: str = ""
    description: str = ""
    tech: List[str] = []
    link: str = ""


class ResumeProfileUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    linkedin_url: Optional[str] = None
    github_url: Optional[str] = None
    portfolio_url: Optional[str] = None
    summary: Optional[str] = None
    target_career_id: Optional[int] = None
    target_job_id: Optional[int] = None
    experience: Optional[List[ExperienceItem]] = None
    education: Optional[List[EducationItem]] = None
    certifications: Optional[List[CertificationItem]] = None
    projects: Optional[List[ResumeProjectItem]] = None
    achievements: Optional[List[str]] = None
    selected_skill_ids: Optional[List[int]] = None


class ResumeAnalysis(BaseModel):
    jd_keywords: List[str] = []
    matched_skills: List[str] = []
    missing_keywords: List[str] = []
    keyword_coverage: float = 0


class ResumeResponse(BaseModel):
    profile: Dict[str, Any]
    suggested_skills: List[Dict[str, Any]] = []
    analysis: ResumeAnalysis = ResumeAnalysis()
    updated_at: Optional[datetime] = None


# ----------------------------------------------------------------- notifications
class NotificationResponse(BaseModel):
    id: int
    type: str
    title: str
    body: str = ""
    link: str = ""
    is_read: bool = False
    created_at: datetime

    class Config:
        from_attributes = True


# ----------------------------------------------------------------- resources
class ResourceListResponse(BaseModel):
    items: List[Any]
    total: int
