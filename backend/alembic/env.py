"""Alembic migration environment.

The database URL comes from the application configuration (DATABASE_URL), or
from TEST_DATABASE_URL when APP_ENV=testing. It is never hardcoded here.
"""

from logging.config import fileConfig

from sqlalchemy import create_engine, pool

from alembic import context
from app.core.settings import get_settings
from app.db.models.system_metadata import Base

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def _database_url() -> str:
    settings = get_settings()
    if settings.app_env == "testing":
        if not settings.test_database_url:
            raise RuntimeError("TEST_DATABASE_URL is required when APP_ENV=testing")
        return settings.test_database_url
    if not settings.database_url:
        raise RuntimeError("DATABASE_URL is required")
    return settings.database_url


def run_migrations_offline() -> None:
    context.configure(
        url=_database_url(),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    engine = create_engine(_database_url(), poolclass=pool.NullPool)
    with engine.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )
        with context.begin_transaction():
            context.run_migrations()
    engine.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
