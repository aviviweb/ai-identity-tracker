import os
import sys

repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir))
backend_path = os.path.join(repo_root, "backend")
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

from app.db.init_db import init_db


def main() -> None:
    # Ensure tables exist using SQLAlchemy metadata
    init_db()
    print("init_ok")


if __name__ == "__main__":
    main()


