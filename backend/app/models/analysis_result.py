from sqlalchemy import JSON, String
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base


class AnalysisResult(Base):
    __tablename__ = "analysis_results"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    subject_ids: Mapped[dict] = mapped_column(JSON)
    scores: Mapped[dict] = mapped_column(JSON)
    summary: Mapped[str] = mapped_column(String(1024))
    created_by: Mapped[str] = mapped_column(String(255))

