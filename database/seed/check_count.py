import os
import sys

repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir))
backend_path = os.path.join(repo_root, "backend")
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

from sqlalchemy import text
from app.db.session import engine


def main() -> None:
    with engine.connect() as conn:
        count = conn.execute(text("select count(*) from demo_profiles")).scalar()  # type: ignore
        print(f"count_demo_profiles {count}")


if __name__ == "__main__":
    main()


