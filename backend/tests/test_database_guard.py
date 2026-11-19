"""Fail-closed test database guard tests.

Positive case: the approved testing target passes against the real database.
Negative cases: every invalid configuration must fail BEFORE any migration,
fixture, write or cleanup can run. Static rejections are proven to never open
a connection (a spy asserts psycopg.connect is not called). Connection failure
and live identity mismatch are exercised with mocked connections.
"""

from __future__ import annotations

from unittest.mock import MagicMock

import psycopg
import pytest

from app.core.database_safety import (
    DatabaseGuardError,
    parse_test_target,
    verify_test_database_identity,
)


def _url(
    host: str = "localhost",
    port: int = 5432,
    db: str = "mini_ems_test",
    user: str = "mini_ems_test",
) -> str:
    return f"postgresql+psycopg://{user}:pw@{host}:{port}/{db}"


@pytest.fixture
def testing_env(monkeypatch: pytest.MonkeyPatch) -> pytest.MonkeyPatch:
    monkeypatch.setenv("APP_ENV", "testing")
    monkeypatch.setenv("TEST_DATABASE_HOST", "localhost")
    monkeypatch.setenv("TEST_DATABASE_URL", _url())
    return monkeypatch


@pytest.fixture
def connect_spy(monkeypatch: pytest.MonkeyPatch) -> MagicMock:
    spy = MagicMock()
    monkeypatch.setattr(psycopg, "connect", spy)
    return spy


class _FakeCursor:
    def __init__(self, row: tuple[str, str]) -> None:
        self._row = row

    def execute(self, sql: str) -> None:  # noqa: ARG002 - identity query only
        return None

    def fetchone(self) -> tuple[str, str]:
        return self._row

    def __enter__(self) -> _FakeCursor:
        return self

    def __exit__(self, *exc: object) -> bool:
        return False


class _FakeConn:
    def __init__(self, row: tuple[str, str]) -> None:
        self._row = row

    def cursor(self) -> _FakeCursor:
        return _FakeCursor(self._row)

    def __enter__(self) -> _FakeConn:
        return self

    def __exit__(self, *exc: object) -> bool:
        return False


# --- Positive case (real connection) ---------------------------------------


def test_approved_target_passes() -> None:
    target = parse_test_target()
    assert target.database == "mini_ems_test"
    assert target.user == "mini_ems_test"
    assert target.host == "localhost"
    assert target.port == 5432
    verify_test_database_identity()


# --- Static rejections: must fail before any connection --------------------


def test_missing_app_env_rejected(testing_env: pytest.MonkeyPatch, connect_spy: MagicMock) -> None:
    testing_env.setenv("APP_ENV", "development")
    with pytest.raises(DatabaseGuardError, match="APP_ENV"):
        parse_test_target()
    connect_spy.assert_not_called()


def test_missing_test_url_rejected(testing_env: pytest.MonkeyPatch, connect_spy: MagicMock) -> None:
    testing_env.delenv("TEST_DATABASE_URL", raising=False)
    with pytest.raises(DatabaseGuardError, match="TEST_DATABASE_URL"):
        parse_test_target()
    connect_spy.assert_not_called()


def test_missing_expected_host_rejected(
    testing_env: pytest.MonkeyPatch, connect_spy: MagicMock
) -> None:
    testing_env.delenv("TEST_DATABASE_HOST", raising=False)
    with pytest.raises(DatabaseGuardError, match="TEST_DATABASE_HOST"):
        parse_test_target()
    connect_spy.assert_not_called()


def test_incorrect_hostname_rejected(
    testing_env: pytest.MonkeyPatch, connect_spy: MagicMock
) -> None:
    testing_env.setenv("TEST_DATABASE_URL", _url(host="other-host"))
    with pytest.raises(DatabaseGuardError, match="hostname"):
        parse_test_target()
    connect_spy.assert_not_called()


def test_missing_hostname_rejected(testing_env: pytest.MonkeyPatch, connect_spy: MagicMock) -> None:
    testing_env.setenv(
        "TEST_DATABASE_URL", "postgresql+psycopg://mini_ems_test:pw@:5432/mini_ems_test"
    )
    with pytest.raises(DatabaseGuardError, match="hostname"):
        parse_test_target()
    connect_spy.assert_not_called()


def test_incorrect_database_name_rejected(
    testing_env: pytest.MonkeyPatch, connect_spy: MagicMock
) -> None:
    testing_env.setenv("TEST_DATABASE_URL", _url(db="other_db"))
    with pytest.raises(DatabaseGuardError, match="database"):
        parse_test_target()
    connect_spy.assert_not_called()


def test_incorrect_port_rejected(testing_env: pytest.MonkeyPatch, connect_spy: MagicMock) -> None:
    testing_env.setenv("TEST_DATABASE_URL", _url(port=5433))
    with pytest.raises(DatabaseGuardError, match="port"):
        parse_test_target()
    connect_spy.assert_not_called()


def test_incorrect_username_rejected(
    testing_env: pytest.MonkeyPatch, connect_spy: MagicMock
) -> None:
    testing_env.setenv("TEST_DATABASE_URL", _url(user="postgres"))
    with pytest.raises(DatabaseGuardError, match="role"):
        parse_test_target()
    connect_spy.assert_not_called()


def test_development_database_target_rejected(
    testing_env: pytest.MonkeyPatch, connect_spy: MagicMock
) -> None:
    testing_env.setenv("TEST_DATABASE_URL", _url(db="mini_ems_dev"))
    with pytest.raises(DatabaseGuardError, match="database"):
        verify_test_database_identity()
    connect_spy.assert_not_called()


def test_production_database_target_rejected(
    testing_env: pytest.MonkeyPatch, connect_spy: MagicMock
) -> None:
    testing_env.setenv("TEST_DATABASE_URL", _url(db="mini_ems_prod"))
    with pytest.raises(DatabaseGuardError, match="database"):
        verify_test_database_identity()
    connect_spy.assert_not_called()


def test_wrong_scheme_rejected(testing_env: pytest.MonkeyPatch, connect_spy: MagicMock) -> None:
    testing_env.setenv(
        "TEST_DATABASE_URL", "postgresql://mini_ems_test:pw@localhost:5432/mini_ems_test"
    )
    with pytest.raises(DatabaseGuardError, match="must use postgresql"):
        parse_test_target()
    connect_spy.assert_not_called()


# --- Connection failure after successful static validation -----------------


def test_connection_failure_fails_closed(
    testing_env: pytest.MonkeyPatch, monkeypatch: pytest.MonkeyPatch
) -> None:
    def _raise(*args: object, **kwargs: object) -> None:
        raise psycopg.OperationalError("simulated connection failure")

    monkeypatch.setattr(psycopg, "connect", _raise)
    with pytest.raises(DatabaseGuardError, match="could not connect"):
        verify_test_database_identity()


# --- Live identity mismatch after a successful connection ------------------


def test_live_database_mismatch_rejected(
    testing_env: pytest.MonkeyPatch, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(
        psycopg, "connect", lambda *a, **k: _FakeConn(("wrong_db", "mini_ems_test"))
    )
    with pytest.raises(DatabaseGuardError, match="actual database"):
        verify_test_database_identity()


def test_live_role_mismatch_rejected(
    testing_env: pytest.MonkeyPatch, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(
        psycopg, "connect", lambda *a, **k: _FakeConn(("mini_ems_test", "wrong_user"))
    )
    with pytest.raises(DatabaseGuardError, match="actual role"):
        verify_test_database_identity()
