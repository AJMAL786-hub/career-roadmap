from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


# ----------------------------------------------------------------- careers
class CareerPathResponse(BaseModel):
    id: int
    title: str
    slug: str
    description: str = ""
    icon: str = "briefcase"
    color: str = "#6366f1"
    difficulty: str = "intermediate"
    estimated_hours: int = 0
    typical_roles: List[str] = []
    major_technologies: List[str] = []
    skill_count: int = 0

    class Config:
        from_attributes = True


class RoadmapEdgeResponse(BaseModel):
    id: int
    source_skill_id: int
    target_skill_id: int

    class Config:
        from_attributes = True


class RoadmapNodeResponse(BaseModel):
    id: int
    skill_id: int
    position_x: float
    position_y: float
    layer: int
    skill: "SkillResponse"
    user_status: str = "not_started"

    class Config:
        from_attributes = True


class RoadmapResponse(BaseModel):
    career_path: CareerPathResponse
    nodes: List[RoadmapNodeResponse]
    edges: List[RoadmapEdgeResponse]


# ----------------------------------------------------------------- skills
class SkillAliasResponse(BaseModel):
    id: int
    alias: str

    class Config:
        from_attributes = True


class ResourceResponse(BaseModel):
    id: int
    title: str
    url: str = ""
    resource_type: str = "docs"
    platform: str = ""
    is_free: bool = True
    difficulty: str = "beginner"
    estimated_hours: float = 0
    description: str = ""

    class Config:
        from_attributes = True


class SkillResponse(BaseModel):
    id: int
    career_path_id: int
    name: str
    slug: str
    description: str = ""
    why_important: str = ""
    level: str = "fundamental"
    category: str = "technical"
    priority: str = "recommended"
    estimated_hours: float = 10
    is_custom: int = 0

    class Config:
        from_attributes = True


class SkillDetailResponse(SkillResponse):
    aliases: List[SkillAliasResponse] = []
    prerequisites: List[dict] = []   # [{skill_id, name, status}]
    dependents: List[dict] = []      # skills that require this one
    resources: List[ResourceResponse] = []
    user_state: Dict[str, Any] = {}  # {status, progress, confidence, notes, ...}


class SkillCreateRequest(BaseModel):
    career_path_id: int
    name: str = Field(min_length=2, max_length=80)
    description: str = Field(default="", max_length=2000)
    why_important: str = ""
    level: str = "fundamental"
    category: str = "technical"
    priority: str = "recommended"
    estimated_hours: float = Field(default=10, gt=0, le=1000)
    prerequisites: List[int] = []


class EvidenceCreate(BaseModel):
    title: str = Field(min_length=1, max_length=160)
    description: str = ""
    url: str = ""
    evidence_type: str = "link"  # link | certificate | project | note


class EvidenceResponse(BaseModel):
    id: int
    title: str
    description: str = ""
    url: str = ""
    evidence_type: str = "link"
    created_at: datetime

    class Config:
        from_attributes = True


class SkillProgressUpdate(BaseModel):
    status: str = Field(pattern="^(not_started|in_progress|completed)$")
    progress: int = Field(default=0, ge=0, le=100)
    notes: Optional[str] = None
    confidence: Optional[int] = Field(default=None, ge=1, le=5)
    certificate_name: Optional[str] = None
    github_url: Optional[str] = None


class UserSkillResponse(BaseModel):
    id: int
    user_id: int
    skill_id: int
    status: str
    progress: int
    confidence: int = 0
    notes: str = ""
    certificate_name: str = ""
    github_url: str = ""
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ----------------------------------------------------------------- study sessions
class StudySessionCreate(BaseModel):
    skill_id: Optional[int] = None
    duration_minutes: int = Field(ge=1, le=1440)
    notes: str = ""
    session_date: Optional[datetime] = None


class StudySessionResponse(BaseModel):
    id: int
    skill_id: Optional[int] = None
    duration_minutes: int
    notes: str = ""
    session_date: datetime

    class Config:
        from_attributes = True


# ----------------------------------------------------------------- dashboard
class DashboardResponse(BaseModel):
    target_career: Optional[Dict[str, Any]] = None
    overall_progress: float = 0
    total_skills: int = 0
    completed_skills: int = 0
    in_progress_skills: int = 0
    remaining_skills: int = 0
    estimated_remaining_hours: float = 0
    category_progress: Dict[str, float] = {}
    current_streak: int = 0
    longest_streak: int = 0
    total_study_minutes: int = 0
    weekly_study: List[Dict[str, Any]] = []
    recommended_next: List[Dict[str, Any]] = []
    job_readiness_score: float = 0
    recent_activity: List[Dict[str, Any]] = []
    latest_jobs: List[Dict[str, Any]] = []
    top_gaps: List[Dict[str, Any]] = []
    gamification: Dict[str, Any] = {}
