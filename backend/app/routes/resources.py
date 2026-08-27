from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.models.learning import LearningResource
from app.models.skill import Skill
from app.schemas.career import ResourceResponse
from app.auth import get_optional_user
from app.models.user import User

router = APIRouter(prefix="/resources", tags=["Learning Resources"])

RESOURCE_TYPES = ["docs", "video", "course", "book", "github", "practice", "tutorial", "certification"]


@router.get("", response_model=List[ResourceResponse])
def list_resources(
    career_id: Optional[int] = None,
    resource_type: Optional[str] = None,
    is_free: Optional[bool] = None,
    limit: int = 200,
    user: User = Depends(get_optional_user),
    db: Session = Depends(get_db),
):
    query = (
        db.query(LearningResource)
        .join(Skill, LearningResource.skill_id == Skill.id)
    )
    if career_id:
        query = query.filter(Skill.career_path_id == career_id)
    if resource_type:
        if resource_type not in RESOURCE_TYPES:
            raise HTTPException(status_code=400, detail="Invalid resource type filter")
        query = query.filter(LearningResource.resource_type == resource_type)
    if is_free is not None:
        query = query.filter(LearningResource.is_free == (1 if is_free else 0))
    rows = query.order_by(LearningResource.skill_id.asc(), LearningResource.id.asc())\
        .limit(min(limit, 500)).all()
    return [ResourceResponse.model_validate(r) for r in rows]


@router.get("/skill/{skill_id}", response_model=List[ResourceResponse])
def resources_for_skill(skill_id: int, db: Session = Depends(get_db)):
    skill = db.query(Skill).filter(Skill.id == skill_id).first()
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    rows = db.query(LearningResource).filter(
        LearningResource.skill_id == skill_id).order_by(LearningResource.id.asc()).all()
    return [ResourceResponse.model_validate(r) for r in rows]
