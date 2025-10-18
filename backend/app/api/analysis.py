from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import List
from sqlalchemy.orm import Session
from app.services.investigator import analyze_text, analyze_images, correlate_profiles
from app.dependencies.db import get_db
from app.models.analysis_result import AnalysisResult
from app.models.history import History
from app.auth.deps import get_current_subject

router = APIRouter()


class TextAnalysisRequest(BaseModel):
    texts: List[List[str]]


class ImageAnalysisRequest(BaseModel):
    image_urls: list[str]


class CorrelateRequest(BaseModel):
    text_groups: List[List[str]] = []
    image_urls: List[str] = []


@router.post("/text")
def analyze_text_endpoint(req: TextAnalysisRequest):
    return analyze_text(req.texts)


@router.post("/image")
def analyze_image_endpoint(req: ImageAnalysisRequest):
    return analyze_images(req.image_urls)


@router.post("/correlate")
def correlate_endpoint(req: CorrelateRequest):
    return correlate_profiles(req.text_groups, req.image_urls)


class RunRequest(BaseModel):
    subject_ids: List[str]
    text_groups: List[List[str]]
    image_urls: List[str]
    created_by: str = "demo@user"


@router.post("/run")
def run_and_store(req: RunRequest, db: Session = Depends(get_db), sub: str | None = Depends(get_current_subject)):
    result = correlate_profiles(req.text_groups, req.image_urls)
    row = AnalysisResult(
        subject_ids={"ids": req.subject_ids},
        scores={"score": result.get("score"), "components": result.get("components", {})},
        summary=result.get("summary", ""),
        created_by=sub or req.created_by,
    )
    db.add(row)
    db.add(
        History(
            user_id=0,
            action="analysis_run",
            meta_json={
                "result_id": None,
                "score": result.get("score"),
                "components": result.get("components", {}),
            },
        )
    )
    db.commit()
    db.refresh(row)
    # Update history row with result_id now that we have it
    db.add(
        History(
            user_id=0,
            action="analysis_stored",
            meta_json={"result_id": row.id},
        )
    )
    db.commit()
    return {"id": row.id, **result}


