from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Local imports
from app.config import get_settings
from app.api.health import router as health_router
from app.auth.router import router as auth_router
from app.api.analysis import router as analysis_router
from app.db.init_db import init_db
from app.api.profiles import router as profiles_router
from app.api.history import router as history_router
from app.api.results import router as results_router


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title="AI Identity Tracker API", version="0.1.0")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(health_router)
    app.include_router(auth_router, prefix="/auth", tags=["auth"])
    app.include_router(analysis_router, prefix="/analysis", tags=["analysis"])
    app.include_router(profiles_router)
    app.include_router(history_router)
    app.include_router(results_router)

    @app.on_event("startup")
    def on_startup() -> None:
        # Create tables if not exist (SQLite dev fallback)
        init_db()

    return app


app = create_app()


