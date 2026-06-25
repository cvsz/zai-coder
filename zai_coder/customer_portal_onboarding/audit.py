"""Customer portal audit log."""

from __future__ import annotations

import json
import sqlite3
import uuid
from pathlib import Path

from .models import CustomerAuditEvent


SCHEMA = """
CREATE TABLE IF NOT EXISTS customer_audit_events (
    id TEXT PRIMARY KEY,
    actor TEXT NOT NULL,
    action TEXT NOT NULL,
    target TEXT NOT NULL,
    customer_id TEXT NOT NULL,
    org_id TEXT NOT NULL,
    workspace_id TEXT NOT NULL,
    payload_json TEXT NOT NULL,
    created_at TEXT NOT NULL
);
"""


class CustomerAuditLog:
    def __init__(self, db_path: str | Path = "data/customer-portal.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(self.db_path) as con:
            con.executescript(SCHEMA)

    def record(self, actor: str, action: str, target: str, payload: dict | None = None, customer_id: str = "cust_local", org_id: str = "org_local", workspace_id: str = "ws_default") -> CustomerAuditEvent:
        event = CustomerAuditEvent(f"cae_{uuid.uuid4().hex[:12]}", actor, action, target, customer_id, org_id, workspace_id, payload or {})
        with sqlite3.connect(self.db_path) as con:
            con.execute(
                """
                INSERT INTO customer_audit_events
                (id, actor, action, target, customer_id, org_id, workspace_id, payload_json, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (event.id, event.actor, event.action, event.target, event.customer_id, event.org_id, event.workspace_id, json.dumps(event.payload, sort_keys=True), event.created_at),
            )
        return event

    def list_events(self, customer_id: str | None = None, limit: int = 100) -> list[dict]:
        with sqlite3.connect(self.db_path) as con:
            if customer_id:
                rows = con.execute(
                    """
                    SELECT id, actor, action, target, customer_id, org_id, workspace_id, payload_json, created_at
                    FROM customer_audit_events WHERE customer_id=? ORDER BY created_at DESC LIMIT ?
                    """,
                    (customer_id, limit),
                ).fetchall()
            else:
                rows = con.execute(
                    """
                    SELECT id, actor, action, target, customer_id, org_id, workspace_id, payload_json, created_at
                    FROM customer_audit_events ORDER BY created_at DESC LIMIT ?
                    """,
                    (limit,),
                ).fetchall()
        return [
            {"id": r[0], "actor": r[1], "action": r[2], "target": r[3], "customer_id": r[4], "org_id": r[5], "workspace_id": r[6], "payload": json.loads(r[7]), "created_at": r[8]}
            for r in rows
        ]
