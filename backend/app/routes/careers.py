from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from typing import List
from app.database import get_db
from app.models.career import CareerPath
from app.models.skill import RoadmapNode, RoadmapEdge, Skill
from app.auth import get_current_user, get_optional_user
from app.models.user import User
from app.schemas.career import (
    CareerPathResponse, RoadmapResponse, RoadmapNodeResponse,
    RoadmapEdgeResponse,
)
import json

router = APIRouter(prefix="/careers", tags=["Careers"])


def _career_response(career: CareerPath) -> CareerPathResponse:
    return CareerPathResponse(
        id=career.id,
        title=career.title,
        slug=career.slug,
        description=career.description or "",
        icon=career.icon,
        color=career.color,
        difficulty=career.difficulty or "intermediate",
        estimated_hours=career.estimated_hours or 0,
        typical_roles=json.loads(career.typical_roles or "[]"),
        major_technologies=json.loads(career.major_technologies or "[]"),
        skill_count=len(career.skills),
    )


@router.get("", response_model=List[CareerPathResponse])
def list_careers(db: Session = Depends(get_db)):
    careers = db.query(CareerPath).options(joinedload(CareerPath.skills)).all()
    return [_career_response(c) for c in sorted(careers, key=lambda c: c.id)]


@router.get("/{career_id}", response_model=CareerPathResponse)
def get_career(career_id: int, db: Session = Depends(get_db)):
    career = db.query(CareerPath).filter(CareerPath.id == career_id).first()
    if not career:
        raise HTTPException(status_code=404, detail="Career path not found")
    return _career_response(career)


@router.get("/by-slug/{slug}", response_model=CareerPathResponse)
def get_career_by_slug(slug: str, db: Session = Depends(get_db)):
    career = db.query(CareerPath).filter(CareerPath.slug == slug).first()
    if not career:
        raise HTTPException(status_code=404, detail="Career path not found")
    return _career_response(career)


@router.get("/{career_id}/roadmap", response_model=RoadmapResponse)
def get_roadmap(
    career_id: int,
    user: User = Depends(get_optional_user),
    db: Session = Depends(get_db),
):
    from datetime import timezone as tz

    career = db.query(CareerPath).filter(CareerPath.id == career_id).first()
    if not career:
        raise HTTPException(status_code=404, detail="Career path not found")

    nodes = (
        db.query(RoadmapNode)
        .options(joinedload(RoadmapNode.skill))
        .filter(RoadmapNode.career_path_id == career_id)
        .order_by(RoadmapNode.layer.asc(), RoadmapNode.position_y.asc())
        .all()
    )
    edges = db.query(RoadmapEdge).filter(RoadmapEdge.career_path_id == career_id).all()

    user_status: dict = {}
    if user:
        from app.models.skill import UserSkill
        rows = (
            db.query(UserSkill)
            .filter(
                UserSkill.user_id == user.id,
                UserSkill.skill_id.in_([n.skill_id for n in nodes]) if nodes else False,
            )
            .all()
        )
        user_status = {r.skill_id: r.status for r in rows}

    node_responses = [
        RoadmapNodeResponse(
            id=n.id,
            skill_id=n.skill_id,
            skill=n.skill,
            position_x=n.position_x,
            position_y=n.position_y,
            layer=n.layer,
            user_status=user_status.get(n.skill_id, "not_started"),
        )
        for n in nodes
    ]
    edge_responses = [
        RoadmapEdgeResponse(id=e.id, source_skill_id=e.source_skill_id, target_skill_id=e.target_skill_id)
        for e in edges
    ]

    return RoadmapResponse(career_path=_career_response(career), nodes=node_responses, edges=edge_responses)
