"""Admin console audit log."""

from __future__ import annotations

import json
import sqlite3
import uuid
from pathlib import Path

from .models import AdminAuditEvent


SCHEMA = """
CREATE TABLE IF NOT EXISTS admin_audit_events (
    id TEXT PRIMARY KEY,
    actor TEXT NOT NULL,
    action TEXT NOT NULL,
    target TEXT NOT NULL,
    org_id TEXT NOT NULL,
    workspace_id TEXT NOT NULL,
    payload_json TEXT NOT NULL,
    created_at TEXT NOT NULL
);
"""


class AdminAuditLog:
    def __init__(self, db_path: str | Path = "data/enterprise-admin-console.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(self.db_path) as con:
            con.executescript(SCHEMA)

    def record(self, actor: str, action: str, target: str, payload: dict | None = None, org_id: str = "org_local", workspace_id: str = "ws_default") -> AdminAuditEvent:
        event = AdminAuditEvent(f"aae_{uuid.uuid4().hex[:12]}", actor, action, target, org_id, workspace_id, payload or {})
        with sqlite3.connect(self.db_path) as con:
            con.execute(
                """
                INSERT INTO admin_audit_events
                (id, actor, action, target, org_id, workspace_id, payload_json, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (event.id, event.actor, event.action, event.target, event.org_id, event.workspace_id, json.dumps(event.payload, sort_keys=True), event.created_at),
            )
        return event

    def list_events(self, org_id: str | None = None, limit: int = 100) -> list[dict]:
        with sqlite3.connect(self.db_path) as con:
            if org_id:
                rows = con.execute(
                    """
                    SELECT id, actor, action, target, org_id, workspace_id, payload_json, created_at
                    FROM admin_audit_events WHERE org_id=? ORDER BY created_at DESC LIMIT ?
                    """,
                    (org_id, limit),
                ).fetchall()
            else:
                rows = con.execute(
                    """
                    SELECT id, actor, action, target, org_id, workspace_id, payload_json, created_at
                    FROM admin_audit_events ORDER BY created_at DESC LIMIT ?
                    """,
                    (limit,),
                ).fetchall()
        return [
            {"id": r[0], "actor": r[1], "action": r[2], "target": r[3], "org_id": r[4], "workspace_id": r[5], "payload": json.loads(r[6]), "created_at": r[7]}
            for r in rows
        ]
