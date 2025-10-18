import os
import sys

repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir))
backend_path = os.path.join(repo_root, "backend")
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.demo_profile import DemoProfile


def main() -> None:
    demo_profiles = [
        DemoProfile(
            platform="twitter",
            handle="@tech_guru_42",
            display_name="Tech Guru",
            avatar_url="https://example.com/avatars/tg.png",
            bio="AI, gadgets, and coffee.",
            sample_posts={"posts": ["AI is changing the world 🤖", "Love my new keyboard!" ]},
        ),
        DemoProfile(
            platform="instagram",
            handle="photo_vibes",
            display_name="Photo Vibes",
            avatar_url="https://example.com/avatars/pv.png",
            bio="Street photography & vibes.",
            sample_posts={"posts": ["Sunset shots are life 🌇", "New lens review"]},
        ),
        DemoProfile(
            platform="tiktok",
            handle="short_skits",
            display_name="Skits Channel",
            avatar_url="https://example.com/avatars/ss.png",
            bio="Comedy skits and trends.",
            sample_posts={"posts": ["New skit up! 😂", "Trend remix"]},
        ),
    ]

    with SessionLocal() as session:  # type: Session
        for p in demo_profiles:
            session.add(p)
        session.commit()

    print("seed_ok")


if __name__ == "__main__":
    main()


