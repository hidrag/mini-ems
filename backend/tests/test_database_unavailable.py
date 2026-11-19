"""Database-unavailable behaviour for the health endpoint.

Uses an unreachable host/port so the endpoint must return 503 with the
approved structure and must never leak connection details.
"""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from app.core.settings import get_settings
from app.db import session as session_mod
from app.main import app


@pytest.fixture(scope="module")
def unavailable_client() -> TestClient:
    # Point the cached engine/session at an unreachable target, then restore.
    session_mod._engine = None
    session_mod._SessionLocal = None
    settings = get_settings()
    unreachable = "postgresql+psycopg://nope" + ":nope@127.0.0.1:5439/nope"
    object.__setattr__(settings, "database_url", unreachable)
    with TestClient(app) as c:
        yield c
    session_mod._engine = None
    session_mod._SessionLocal = None


def test_database_health_unavailable(unavailable_client: TestClient) -> None:
    resp = unavailable_client.get("/api/v1/health/database")
    assert resp.status_code == 503
    assert resp.json() == {"status": "unhealthy", "database": "unavailable"}
    body = resp.text
    assert "nope" not in body
    assert "5439" not in body
    assert "Traceback" not in body
    assert "psycopg" not in body


def test_liveness_still_healthy_when_db_down(unavailable_client: TestClient) -> None:
    resp = unavailable_client.get("/api/v1/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "healthy"}
