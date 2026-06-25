"""Usage accounting for agent runs, media jobs, and API requests."""

from __future__ import annotations

import sqlite3
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import List


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


SCHEMA = """
CREATE TABLE IF NOT EXISTS usage_events (
    id TEXT PRIMARY KEY,
    account_id TEXT NOT NULL,
    workspace_id TEXT NOT NULL,
    resource TEXT NOT NULL,
    units INTEGER NOT NULL,
    source TEXT NOT NULL,
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL
);
"""


@dataclass(frozen=True)
class UsageEvent:
    id: str
    account_id: str
    workspace_id: str
    resource: str
    units: int
    source: str
    metadata_json: str = "{}"
    created_at: str = field(default_factory=now_iso)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "account_id": self.account_id,
            "workspace_id": self.workspace_id,
            "resource": self.resource,
            "units": self.units,
            "source": self.source,
            "metadata_json": self.metadata_json,
            "created_at": self.created_at,
        }


class UsageStore:
    def __init__(self, db_path: str | Path):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(self.db_path) as con:
            con.executescript(SCHEMA)

    def record(self, account_id: str, workspace_id: str, resource: str, units: int, source: str, metadata_json: str = "{}") -> UsageEvent:
        if units <= 0:
            raise ValueError("units must be positive")
        event = UsageEvent(
            id=str(uuid.uuid4()),
            account_id=account_id,
            workspace_id=workspace_id,
            resource=resource,
            units=units,
            source=source,
            metadata_json=metadata_json,
        )
        with sqlite3.connect(self.db_path) as con:
            con.execute(
                """
                INSERT INTO usage_events
                (id, account_id, workspace_id, resource, units, source, metadata_json, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    event.id,
                    event.account_id,
                    event.workspace_id,
                    event.resource,
                    event.units,
                    event.source,
                    event.metadata_json,
                    event.created_at,
                ),
            )
        return event

    def total(self, account_id: str, resource: str) -> int:
        with sqlite3.connect(self.db_path) as con:
            value = con.execute(
                "SELECT COALESCE(SUM(units), 0) FROM usage_events WHERE account_id = ? AND resource = ?",
                (account_id, resource),
            ).fetchone()[0]
        return int(value)
