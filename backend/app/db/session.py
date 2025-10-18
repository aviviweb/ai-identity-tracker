from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv


DEFAULT_SQLITE_URL = "sqlite:///./dev.db"


def get_database_url() -> str:
    return os.getenv("DATABASE_URL", DEFAULT_SQLITE_URL)


load_dotenv()  # ensure .env is loaded before reading DATABASE_URL
engine = create_engine(get_database_url(), future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)


