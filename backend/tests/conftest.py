"""Test bootstrap.

Every test session starts by running the fail-closed database guard: the test
target must be an approved isolated testing database before any fixture,
migration, write or cleanup may execute.
"""

from __future__ import annotations

import os

import pytest

from app.core.database_safety import (
    TestTarget,
    assert_test_database_safe,
    parse_test_target,
)
from app.core.settings import Settings, get_settings

# The dedicated test connection is supplied by environment configuration
# (see .env.example / CI). The password is never embedded in a URL literal.
TEST_DATABASE = os.environ["TEST_DATABASE"]
TEST_URL = "postgresql+psycopg://" + TEST_DATABASE


def pytest_configure(config: pytest.Config) -> None:
    """Run the guard once, before any test collection or fixture setup."""
    os.environ["APP_ENV"] = "testing"
    os.environ["TEST_DATABASE_URL"] = TEST_URL
    os.environ.setdefault("TEST_DATABASE_HOST", "localhost")
    assert_test_database_safe()


@pytest.fixture(scope="session")
def settings() -> Settings:
    get_settings.cache_clear()
    return get_settings()


@pytest.fixture(scope="session")
def test_target() -> TestTarget:
    return parse_test_target()
