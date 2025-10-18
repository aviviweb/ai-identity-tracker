from typing import List

from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.responses import StreamingResponse, JSONResponse
from sqlalchemy.orm import Session

from app.dependencies.db import get_db
from app.models.analysis_result import AnalysisResult
from app.auth.deps import get_current_subject


router = APIRouter(prefix="/results", tags=["results"])


@router.get("")
def list_results(limit: int = 20, offset: int = 0, mine: bool = False, db: Session = Depends(get_db), sub: str | None = Depends(get_current_subject), response: Response | None = None) -> List[dict]:
    q = db.query(AnalysisResult)
    if mine and sub:
        q = q.filter(AnalysisResult.created_by == sub)
    total = q.count()
    rows = (
        q.order_by(AnalysisResult.id.desc())
        .offset(max(0, offset))
        .limit(max(1, min(limit, 100)))
        .all()
    )
    if response is not None:
        response.headers["X-Total-Count"] = str(total)
    return [
        {
            "id": r.id,
            "subject_ids": r.subject_ids,
            "scores": r.scores,
            "summary": r.summary,
            "created_by": r.created_by,
        }
        for r in rows
    ]


@router.get("/{result_id}")
def get_result(result_id: int, db: Session = Depends(get_db)) -> dict:
    r = db.get(AnalysisResult, result_id)
    if not r:
        raise HTTPException(status_code=404, detail="Not found")
    return {
        "id": r.id,
        "subject_ids": r.subject_ids,
        "scores": r.scores,
        "summary": r.summary,
        "created_by": r.created_by,
    }


@router.get("/{result_id}/export")
def export_result(result_id: int, format: str = "json", db: Session = Depends(get_db)) -> dict:
    r = db.get(AnalysisResult, result_id)
    if not r:
        raise HTTPException(status_code=404, detail="Not found")
    if format == "csv":
        content = "id,created_by,score\n%s,%s,%s" % (r.id, r.created_by, r.scores.get("score"))
        return StreamingResponse(iter([content]), media_type="text/csv", headers={
            "Content-Disposition": f"attachment; filename=result_{r.id}.csv"
        })
    return JSONResponse({
        "id": r.id,
        "subject_ids": r.subject_ids,
        "scores": r.scores,
        "summary": r.summary,
        "created_by": r.created_by,
        "format": "json",
    })


