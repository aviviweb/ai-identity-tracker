from logging.config import fileConfig
import os
import sys

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# Ensure backend package is importable
here = os.path.abspath(os.path.dirname(__file__))
repo_root = os.path.abspath(os.path.join(here, os.pardir, os.pardir))
backend_path = os.path.join(repo_root, "backend")
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

from app.db.base import Base  # type: ignore  # noqa: E402
from app.db.session import get_database_url  # type: ignore  # noqa: E402
# Import models so that Base.metadata is populated for autogenerate
from app.models.user import User  # type: ignore  # noqa: F401,E402
from app.models.demo_profile import DemoProfile  # type: ignore  # noqa: F401,E402
from app.models.analysis_result import AnalysisResult  # type: ignore  # noqa: F401,E402
from app.models.history import History  # type: ignore  # noqa: F401,E402

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Target metadata for 'autogenerate'
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = os.getenv("DATABASE_URL", get_database_url())
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    configuration = config.get_section(config.config_ini_section, {})
    configuration["sqlalchemy.url"] = os.getenv("DATABASE_URL", get_database_url())
    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
