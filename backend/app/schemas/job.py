from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class JobAnalyzeRequest(BaseModel):
    title: str = Field(default="", max_length=160)
    company: str = Field(default="", max_length=120)
    location: str = ""
    raw_text: str = Field(min_length=30, max_length=60000)
    save: bool = True


class GapItemSchema(BaseModel):
    canonical: str
    display_name: str
    requirement_type: str
    category: str = "technical"
    user_status: str = "not_started"
    confidence: int = 0
    matched_skill_id: Optional[int] = None
    estimated_hours: float = 8
    priority_score: float = 0
    priority_label: str = "Medium"


class ParsedMeta(BaseModel):
    years_experience: Optional[int] = None
    education: List[str] = []
    certifications: List[str] = []
    soft_skills: List[str] = []
    domains: List[str] = []


class JobAnalysisResponse(BaseModel):
    id: int
    title: str
    company: str
    location: str = ""
    match_score: float
    exact_matches: List[GapItemSchema]
    partial_matches: List[GapItemSchema]
    missing_required: List[GapItemSchema]
    missing_preferred: List[GapItemSchema]
    overqualified: List[GapItemSchema]
    learn_first: List[GapItemSchema]
    parsed_meta: ParsedMeta
    created_at: Optional[datetime] = None


class JobSummaryResponse(BaseModel):
    id: int
    title: str
    company: str
    location: str = ""
    match_score: float
    created_at: datetime

    class Config:
        from_attributes = True


class JobCompareItem(BaseModel):
    job_id: int
    title: str
    company: str
    match_score: float
    skills: Dict[str, str]  # canonical -> "exact" | "partial" | "missing"


class JobCompareResponse(BaseModel):
    jobs: List[JobCompareItem]
    common_missing: List[str]
    union_missing: List[str]
