"""Settings parsing and validation tests."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from app.core.settings import Settings


def test_defaults() -> None:
    s = Settings()
    assert s.app_name == "Mini EMS"
    assert s.app_env in {"development", "testing", "production"}
    assert s.api_host == "127.0.0.1"
    assert s.api_port == 8000


def test_invalid_app_env_rejected() -> None:
    with pytest.raises(ValidationError):
        Settings(_env_file=None, APP_ENV="prod")


def test_database_url_scheme_validated() -> None:
    with pytest.raises(ValidationError):
        Settings(_env_file=None, DATABASE_URL="sqlite:///dev.db")


def test_psycopg_scheme_accepted() -> None:
    s = Settings(
        _env_file=None,
        DATABASE_URL="postgresql+psycopg://u:p@localhost:5432/db",
    )
    assert s.database_url is not None
