from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import APIRouter, Response, HTTPException, Depends
from pydantic import BaseModel, EmailStr
import jwt

from app.config import get_settings
from app.auth.deps import get_current_subject


router = APIRouter()


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


def _create_token(email: str, minutes: int) -> str:
    settings = get_settings()
    payload = {
        "sub": email,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=minutes),
        "iat": datetime.now(timezone.utc),
        "type": "access",
    }
    return jwt.encode(payload, settings.jwt_secret, algorithm="HS256")


@router.post("/register", response_model=AuthResponse)
def register(_: RegisterRequest, response: Response):
    # Placeholder: accept any registration for now
    token = _create_token("demo@user", 30)
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure=False,
        samesite="lax",
        path="/",
    )
    return AuthResponse(access_token=token)


@router.post("/login", response_model=AuthResponse)
def login(_: LoginRequest, response: Response):
    token = _create_token("demo@user", 30)
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure=False,
        samesite="lax",
        path="/",
    )
    return AuthResponse(access_token=token)


@router.post("/logout")
def logout(response: Response):
    response.delete_cookie("access_token", path="/")
    return {"ok": True}


@router.get("/me")
def me(sub: str | None = Depends(get_current_subject)):
    return {"sub": sub}

