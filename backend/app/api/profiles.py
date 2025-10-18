from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.dependencies.db import get_db
from app.models.demo_profile import DemoProfile
from app.schemas.profile import DemoProfileOut
from app.config import get_settings


router = APIRouter(prefix="/profiles", tags=["profiles"])


@router.get("", response_model=list[DemoProfileOut])
def list_profiles(
    mode: str = Query("demo", pattern="^(demo|live)$"),
    db: Session = Depends(get_db),
):
    settings = get_settings()
    if mode == "live" and not settings.demo_mode:
        # Placeholder: no live integration yet
        return []

    rows = db.query(DemoProfile).limit(50).all()
    return rows


