from typing import List, Optional

from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session

from app.dependencies.db import get_db
from app.models.history import History


router = APIRouter(prefix="/history", tags=["history"])


@router.get("")
def list_history(
    limit: int = 20,
    offset: int = 0,
    action: Optional[str] = None,
    user_id: Optional[int] = None,
    db: Session = Depends(get_db),
    response: Response | None = None,
) -> List[dict]:
    q = db.query(History)
    if action:
        q = q.filter(History.action == action)
    if user_id is not None:
        q = q.filter(History.user_id == user_id)
    total = q.count()
    rows = (
        q.order_by(History.id.desc())
        .offset(max(0, offset))
        .limit(max(1, min(limit, 100)))
        .all()
    )
    if response is not None:
        response.headers["X-Total-Count"] = str(total)
    return [
        {
            "id": r.id,
            "user_id": r.user_id,
            "action": r.action,
            "meta_json": r.meta_json,
        }
        for r in rows
    ]


