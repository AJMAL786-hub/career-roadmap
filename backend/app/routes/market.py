from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.career import CareerPath
from app.services.market_provider import market_service, LOCATIONS

router = APIRouter(prefix="/market", tags=["Market Intelligence"])


@router.get("/locations")
def list_locations():
    return {"locations": LOCATIONS}


@router.get("/{career}")
def get_market(career: str, db: Session = Depends(get_db)):
    """career accepts a career slug or id. Data is cached; demo-labelled."""
    if career.isdigit():
        row = db.query(CareerPath).filter(CareerPath.id == int(career)).first()
        if not row:
            raise HTTPException(status_code=404, detail="Career not found")
        slug = row.slug
    else:
        row = db.query(CareerPath).filter(CareerPath.slug == career).first()
        if not row:
            raise HTTPException(status_code=404, detail="Career not found")
        slug = row.slug

    data = market_service.get_market(slug)
    if not data:
        raise HTTPException(status_code=404, detail="No market data for this career yet")
    return data
