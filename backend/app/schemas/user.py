from pydantic import BaseModel, Field, field_validator
from typing import Optional, List, Dict, Any
from datetime import datetime
import re


class UserCreate(BaseModel):
    email: str = Field(max_length=200)
    username: str = Field(min_length=3, max_length=40)
    password: str = Field(min_length=8, max_length=128)
    full_name: str = ""

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        v = v.strip().lower()
        if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", v):
            raise ValueError("Invalid email address")
        return v

    @field_validator("username")
    @classmethod
    def validate_username(cls, v: str) -> str:
        if not re.match(r"^[a-zA-Z0-9_.-]+$", v):
            raise ValueError("Username may only contain letters, numbers, _ . -")
        return v

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        if len(v) < 8 or not any(c.isdigit() for c in v) or not any(c.isalpha() for c in v):
            raise ValueError("Password must be 8+ characters with letters and numbers")
        return v


class UserLogin(BaseModel):
    email: str
    password: str
    remember: bool = True


class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    full_name: str
    avatar_url: str
    auth_provider: str = "local"
    selected_career_id: Optional[int]
    onboarding_completed: bool
    xp: int = 0
    created_at: datetime

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    avatar_url: Optional[str] = None
    selected_career_id: Optional[int] = None
    onboarding_completed: Optional[bool] = None


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


class ProfileStatsResponse(BaseModel):
    user: UserResponse
    gamification: Dict[str, Any] = {}
    achievements: List[Dict[str, Any]] = []
    streak: Dict[str, Any] = {}
