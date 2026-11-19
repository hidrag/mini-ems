"""system_metadata behaviour: updated_at must change on SQLAlchemy updates.

Writes only to the dedicated, guard-validated testing database and removes the
probe row afterwards. created_at must remain unchanged; updated_at must advance.
"""

from __future__ import annotations

import time
import uuid

from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from app.db.models.system_metadata import SystemMetadata
from tests.conftest import TEST_URL


def test_updated_at_changes_on_sqlalchemy_update() -> None:
    engine = create_engine(TEST_URL)
    key = "probe_updated_at_" + uuid.uuid4().hex
    try:
        with Session(engine) as session:
            row = SystemMetadata(key=key, value="initial")
            session.add(row)
            session.commit()
            session.refresh(row)
            created_at = row.created_at
            initial_updated_at = row.updated_at
            assert created_at is not None
            assert initial_updated_at is not None
            assert created_at.tzinfo is not None
            assert initial_updated_at.tzinfo is not None

        # Ensure the UPDATE runs in a later transaction than the INSERT.
        time.sleep(0.02)

        with Session(engine) as session:
            row = session.scalar(select(SystemMetadata).where(SystemMetadata.key == key))
            assert row is not None
            row.value = "changed"
            session.commit()
            session.refresh(row)
            assert row.created_at == created_at
            assert row.updated_at > created_at
            assert row.updated_at != initial_updated_at
    finally:
        with Session(engine) as session:
            row = session.scalar(select(SystemMetadata).where(SystemMetadata.key == key))
            if row is not None:
                session.delete(row)
                session.commit()
        engine.dispose()
