"""Root endpoint (approved Phase 1 contract)."""

from __future__ import annotations

from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def root() -> dict[str, str]:
    """Root welcome endpoint."""
    return {"message": "Mini EMS API", "status": "running"}
