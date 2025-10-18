from sqlalchemy import JSON, String
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base


class History(Base):
    __tablename__ = "history"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column()
    action: Mapped[str] = mapped_column(String(128))
    meta_json: Mapped[dict] = mapped_column(JSON)

