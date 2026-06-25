"""Release audit log."""

from __future__ import annotations

import json
import sqlite3
import uuid
from pathlib import Path

from .models import ReleaseAuditEvent


SCHEMA = """
CREATE TABLE IF NOT EXISTS release_audit_events (
    id TEXT PRIMARY KEY,
    actor TEXT NOT NULL,
    action TEXT NOT NULL,
    target TEXT NOT NULL,
    payload_json TEXT NOT NULL,
    created_at TEXT NOT NULL
);
"""


class ReleaseAuditLog:
    def __init__(self, db_path: str | Path = "data/release-update-center.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(self.db_path) as con:
            con.executescript(SCHEMA)

    def record(self, actor: str, action: str, target: str, payload: dict | None = None) -> ReleaseAuditEvent:
        event = ReleaseAuditEvent(f"rae_{uuid.uuid4().hex[:12]}", actor, action, target, payload or {})
        with sqlite3.connect(self.db_path) as con:
            con.execute(
                """
                INSERT INTO release_audit_events
                (id, actor, action, target, payload_json, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (event.id, event.actor, event.action, event.target, json.dumps(event.payload, sort_keys=True), event.created_at),
            )
        return event

    def list_events(self, limit: int = 100) -> list[dict]:
        with sqlite3.connect(self.db_path) as con:
            rows = con.execute(
                """
                SELECT id, actor, action, target, payload_json, created_at
                FROM release_audit_events ORDER BY created_at DESC LIMIT ?
                """,
                (limit,),
            ).fetchall()
        return [
            {"id": r[0], "actor": r[1], "action": r[2], "target": r[3], "payload": json.loads(r[4]), "created_at": r[5]}
            for r in rows
        ]
