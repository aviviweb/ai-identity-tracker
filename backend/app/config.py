from functools import lru_cache
from pydantic import BaseModel
from typing import List
import os
from dotenv import load_dotenv

# Load env vars from a .env file in the backend directory (if present)
load_dotenv()


class Settings(BaseModel):
    jwt_secret: str = os.getenv("JWT_SECRET", "dev-secret-change")
    cors_origins: List[str] = (
        os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")
    )
    demo_mode: bool = os.getenv("DEMO_MODE", "true").lower() == "true"


@lru_cache
def get_settings() -> Settings:
    return Settings()


