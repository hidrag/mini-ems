"""Migration verification: the applied schema must match the approved table."""

from __future__ import annotations

from alembic.config import Config
from sqlalchemy import create_engine, inspect

from alembic import command
from tests.conftest import TEST_URL


def _apply_migrations() -> None:
    cfg = Config("alembic.ini")
    cfg.set_main_option("script_location", "alembic")
    cfg.set_main_option("sqlalchemy.url", TEST_URL)
    command.upgrade(cfg, "head")


def test_migration_creates_exact_schema() -> None:
    _apply_migrations()
    engine = create_engine(TEST_URL)
    insp = inspect(engine)
    assert set(insp.get_table_names()) == {"system_metadata", "alembic_version"}
    cols = {c["name"]: c for c in insp.get_columns("system_metadata")}
    assert set(cols) == {"id", "key", "value", "created_at", "updated_at"}
    for name in ("id", "key", "value", "created_at", "updated_at"):
        assert cols[name]["nullable"] is False, name
    for col in (cols["created_at"], cols["updated_at"]):
        assert col["type"].timezone is True
    uniques = insp.get_unique_constraints("system_metadata")
    assert any({c for c in u["column_names"]} == {"key"} for u in uniques), "key must be UNIQUE"
    engine.dispose()


def test_migration_is_idempotent() -> None:
    """Running upgrade again must be a no-op (already at head)."""
    _apply_migrations()
