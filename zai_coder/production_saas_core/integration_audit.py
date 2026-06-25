"""Integration audit log."""

from __future__ import annotations

import json
import sqlite3
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path


SCHEMA = """
CREATE TABLE IF NOT EXISTS integration_audit_events (
    id TEXT PRIMARY KEY,
    provider TEXT NOT NULL,
    action TEXT NOT NULL,
    actor TEXT NOT NULL,
    dry_run INTEGER NOT NULL,
    payload_json TEXT NOT NULL,
    created_at TEXT NOT NULL
);
"""


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass(frozen=True)
class IntegrationAuditEvent:
    id: str
    provider: str
    action: str
    actor: str
    dry_run: bool
    payload_json: str
    created_at: str = field(default_factory=now_iso)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "provider": self.provider,
            "action": self.action,
            "actor": self.actor,
            "dry_run": self.dry_run,
            "payload_json": self.payload_json,
            "created_at": self.created_at,
        }


class IntegrationAuditLog:
    def __init__(self, db_path: str | Path):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(self.db_path) as con:
            con.executescript(SCHEMA)

    def record(self, provider: str, action: str, actor: str, payload: dict, dry_run: bool = True) -> IntegrationAuditEvent:
        event = IntegrationAuditEvent(
            id=str(uuid.uuid4()),
            provider=provider,
            action=action,
            actor=actor,
            dry_run=dry_run,
            payload_json=json.dumps(payload, sort_keys=True),
        )
        with sqlite3.connect(self.db_path) as con:
            con.execute(
                """
                INSERT INTO integration_audit_events
                (id, provider, action, actor, dry_run, payload_json, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (event.id, event.provider, event.action, event.actor, int(event.dry_run), event.payload_json, event.created_at),
            )
        return event
