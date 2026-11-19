"""SQLAlchemy engine and session factory."""

from __future__ import annotations

from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.settings import get_settings

_engine = None
_SessionLocal: sessionmaker[Session] | None = None


def _get_engine():
    global _engine
    if _engine is None:
        settings = get_settings()
        if not settings.database_url:
            raise RuntimeError("DATABASE_URL is not configured")
        _engine = create_engine(
            settings.database_url,
            pool_pre_ping=True,
            connect_args={"connect_timeout": 2},
        )
    return _engine


def get_session_local() -> sessionmaker[Session]:
    global _SessionLocal
    if _SessionLocal is None:
        _SessionLocal = sessionmaker(bind=_get_engine(), autoflush=False, expire_on_commit=False)
    return _SessionLocal


def get_db() -> Generator[Session, None, None]:
    """FastAPI dependency yielding a request-scoped database session."""
    session = get_session_local()()
    try:
        yield session
    finally:
        session.close()
