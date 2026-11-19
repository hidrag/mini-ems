"""Health endpoints (approved Phase 1 contract)."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.db.session import get_db

router = APIRouter()

DbSession = Annotated[Session, Depends(get_db)]


@router.get("/health")
def health() -> dict[str, str]:
    """Application liveness endpoint; never depends on PostgreSQL."""
    return {"status": "healthy"}


@router.get("/health/database")
def database_health(db: DbSession) -> JSONResponse:
    """Database connectivity health endpoint.

    Executes ``SELECT 1``. Returns 200 when PostgreSQL is available and 503
    otherwise. Responses never expose connection details or stack traces.
    """
    try:
        db.execute(text("SELECT 1"))
    except Exception:
        return JSONResponse(
            status_code=503,
            content={"status": "unhealthy", "database": "unavailable"},
        )
    return JSONResponse(
        status_code=200,
        content={"status": "healthy", "database": "connected"},
    )
