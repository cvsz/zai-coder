"""Payment audit log."""

from __future__ import annotations

import json
import sqlite3
import uuid
from pathlib import Path

from .models import PaymentAuditEvent


SCHEMA = """
CREATE TABLE IF NOT EXISTS payment_audit_events (
    id TEXT PRIMARY KEY,
    org_id TEXT NOT NULL,
    actor TEXT NOT NULL,
    action TEXT NOT NULL,
    target TEXT NOT NULL,
    provider TEXT NOT NULL,
    payload_json TEXT NOT NULL,
    created_at TEXT NOT NULL
);
"""


class PaymentAuditLog:
    def __init__(self, db_path: str | Path = "data/payment-audit.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(self.db_path) as con:
            con.executescript(SCHEMA)

    def record(self, org_id: str, actor: str, action: str, target: str, provider: str = "sandbox", payload: dict | None = None) -> PaymentAuditEvent:
        event = PaymentAuditEvent(f"pae_{uuid.uuid4().hex[:12]}", org_id, actor, action, target, provider, payload or {})
        with sqlite3.connect(self.db_path) as con:
            con.execute(
                """
                INSERT INTO payment_audit_events
                (id, org_id, actor, action, target, provider, payload_json, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (event.id, event.org_id, event.actor, event.action, event.target, event.provider, json.dumps(event.payload, sort_keys=True), event.created_at),
            )
        return event

    def list_events(self, org_id: str, limit: int = 100) -> list[dict]:
        with sqlite3.connect(self.db_path) as con:
            rows = con.execute(
                """
                SELECT id, org_id, actor, action, target, provider, payload_json, created_at
                FROM payment_audit_events WHERE org_id=?
                ORDER BY created_at DESC LIMIT ?
                """,
                (org_id, limit),
            ).fetchall()
        return [
            {"id": r[0], "org_id": r[1], "actor": r[2], "action": r[3], "target": r[4], "provider": r[5], "payload": json.loads(r[6]), "created_at": r[7]}
            for r in rows
        ]
