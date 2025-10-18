from sqlalchemy import String, JSON
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base


class DemoProfile(Base):
    __tablename__ = "demo_profiles"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    platform: Mapped[str] = mapped_column(String(64))
    handle: Mapped[str] = mapped_column(String(128), index=True)
    display_name: Mapped[str] = mapped_column(String(128))
    avatar_url: Mapped[str] = mapped_column(String(512))
    bio: Mapped[str] = mapped_column(String(1024))
    sample_posts: Mapped[dict] = mapped_column(JSON)

