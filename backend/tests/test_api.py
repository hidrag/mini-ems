"""API contract tests (approved Phase 1 response structures).

The API engine is pointed at the dedicated testing database so the database
health endpoint is exercised against a real, isolated target.
"""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from app.core.settings import get_settings
from app.db import session as session_mod
from app.main import app
from tests.conftest import TEST_URL


@pytest.fixture(scope="module")
def client() -> TestClient:
    session_mod._engine = None
    session_mod._SessionLocal = None
    settings = get_settings()
    object.__setattr__(settings, "database_url", TEST_URL)
    with TestClient(app) as c:
        yield c
    session_mod._engine = None
    session_mod._SessionLocal = None


def test_root(client: TestClient) -> None:
    resp = client.get("/")
    assert resp.status_code == 200
    assert resp.json() == {"message": "Mini EMS API", "status": "running"}


def test_health(client: TestClient) -> None:
    resp = client.get("/api/v1/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "healthy"}


def test_health_database_connected(client: TestClient) -> None:
    resp = client.get("/api/v1/health/database")
    assert resp.status_code == 200
    assert resp.json() == {"status": "healthy", "database": "connected"}


def test_cors_allows_frontend_origin(client: TestClient) -> None:
    resp = client.get(
        "/api/v1/health",
        headers={"Origin": "http://localhost:5173"},
    )
    assert resp.status_code == 200
    assert resp.headers.get("access-control-allow-origin") == "http://localhost:5173"


def test_cors_rejects_unknown_origin(client: TestClient) -> None:
    resp = client.get(
        "/api/v1/health",
        headers={"Origin": "http://evil.example"},
    )
    assert resp.status_code == 200
    assert resp.headers.get("access-control-allow-origin") is None
