"""Fail-closed guard for the automated testing database.

Automated tests must never modify development or production data. Before any
migration, fixture, write or cleanup, this guard validates that the target is
the explicitly approved testing configuration:

1. APP_ENV must be "testing".
2. TEST_DATABASE_URL must be set (never fall back to DATABASE_URL).
3. TEST_DATABASE_HOST must be set (the expected database hostname).
4. The URL is parsed and statically validated WITHOUT connecting: scheme,
   hostname (against TEST_DATABASE_HOST), port, database name and username.
   Every static failure happens before any connection is attempted.
5. Only after static validation succeeds is a connection opened with the
   dedicated test role, and read-only identity checks (current_database(),
   current_user) verify the actual target.
6. Only after every check passes may mutations proceed.

The PostgreSQL role/database permissions provide the second isolation layer:
the dedicated test role has no CONNECT privilege on development or production
databases (see docs/04-database-schema.md).
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from urllib.parse import unquote, urlsplit

import psycopg

# Fixed values approved for the Phase 1 automated testing target.
EXPECTED_DATABASE = "mini_ems_test"
EXPECTED_USER = "mini_ems_test"
EXPECTED_PORT = 5432


class DatabaseGuardError(RuntimeError):
    """Raised when the test database target cannot be validated."""


@dataclass(frozen=True)
class TestTarget:
    """Validated test database target derived from the approved configuration."""

    scheme: str
    host: str
    port: int
    database: str
    user: str


def _require_testing_env() -> None:
    app_env = os.environ.get("APP_ENV")
    if app_env != "testing":
        raise DatabaseGuardError(
            f"APP_ENV must be 'testing' before any test database operation (got {app_env!r})"
        )


def _require_test_url() -> str:
    test_url = os.environ.get("TEST_DATABASE_URL")
    if not test_url:
        raise DatabaseGuardError("TEST_DATABASE_URL is required; never fall back to DATABASE_URL")
    return test_url


def _require_expected_host() -> str:
    expected_host = os.environ.get("TEST_DATABASE_HOST")
    if not expected_host:
        raise DatabaseGuardError(
            "TEST_DATABASE_HOST is required to validate the test database hostname"
        )
    return expected_host


def parse_test_target() -> TestTarget:
    """Parse and statically validate TEST_DATABASE_URL without connecting.

    Validates scheme, hostname (against TEST_DATABASE_HOST), port, database
    name and username. Raises DatabaseGuardError on any missing, malformed or
    mismatched value. No connection is attempted here.
    """
    _require_testing_env()
    test_url = _require_test_url()
    expected_host = _require_expected_host()

    parts = urlsplit(test_url)
    if parts.scheme != "postgresql+psycopg":
        raise DatabaseGuardError("TEST_DATABASE_URL must use postgresql+psycopg://")

    host = parts.hostname or ""
    if not host:
        raise DatabaseGuardError("TEST_DATABASE_URL must include a hostname")
    if host != expected_host:
        raise DatabaseGuardError(
            "TEST_DATABASE_URL hostname does not match TEST_DATABASE_HOST "
            f"({host!r} != {expected_host!r})"
        )

    try:
        port = parts.port or EXPECTED_PORT
    except ValueError as exc:
        raise DatabaseGuardError("TEST_DATABASE_URL has a malformed port") from exc
    if port != EXPECTED_PORT:
        raise DatabaseGuardError(f"TEST_DATABASE_URL must target port {EXPECTED_PORT} (got {port})")

    database = unquote(parts.path.lstrip("/"))
    if database != EXPECTED_DATABASE:
        raise DatabaseGuardError(
            f"TEST_DATABASE_URL must target database '{EXPECTED_DATABASE}' (got {database!r})"
        )

    user = unquote(parts.username or "")
    if user != EXPECTED_USER:
        raise DatabaseGuardError(
            f"TEST_DATABASE_URL must use role '{EXPECTED_USER}' (got {user!r})"
        )

    return TestTarget(
        scheme=parts.scheme,
        host=host,
        port=port,
        database=database,
        user=user,
    )


def verify_test_database_identity() -> None:
    """Connect with the dedicated test role and verify the actual database/user.

    Static validation runs first; only if it passes is a connection opened.
    Read-only identity checks only; no schema, fixture or data mutations.
    """
    target = parse_test_target()
    test_url = os.environ["TEST_DATABASE_URL"]
    # psycopg accepts libpq-style URLs; strip the SQLAlchemy driver suffix.
    conn_url = test_url.replace("postgresql+psycopg://", "postgresql://", 1)
    try:
        with psycopg.connect(conn_url, connect_timeout=5) as conn, conn.cursor() as cur:
            cur.execute("SELECT current_database(), current_user")
            actual_database, actual_user = cur.fetchone()
    except psycopg.Error as exc:
        raise DatabaseGuardError(
            "could not connect to the test database for identity verification"
        ) from exc
    if actual_database != target.database:
        raise DatabaseGuardError(
            "actual database does not match the approved test database "
            f"({actual_database!r} != {target.database!r})"
        )
    if actual_user != target.user:
        raise DatabaseGuardError(
            "actual role does not match the approved test role "
            f"({actual_user!r} != {target.user!r})"
        )


def assert_test_database_safe() -> None:
    """Run the complete guard; raise DatabaseGuardError on any failure."""
    verify_test_database_identity()
