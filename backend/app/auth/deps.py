from typing import Optional

from fastapi import Cookie, HTTPException
import jwt

from app.config import get_settings


def get_current_subject(access_token: Optional[str] = Cookie(default=None)) -> Optional[str]:
    if not access_token:
        return None
    try:
        settings = get_settings()
        payload = jwt.decode(access_token, settings.jwt_secret, algorithms=["HS256"])  # type: ignore
        sub = payload.get("sub")
        if not isinstance(sub, str):
            return None
        return sub
    except Exception as _:
        # Invalid token; treat as anonymous
        return None



