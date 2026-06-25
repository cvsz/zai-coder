"""Usage event ledger."""

from __future__ import annotations

import json
import sqlite3
import uuid
from pathlib import Path

from .models import UsageEvent, BillingAuditEvent


SCHEMA = """
CREATE TABLE IF NOT EXISTS usage_events (
    id TEXT PRIMARY KEY,
    org_id TEXT NOT NULL,
    workspace_id TEXT NOT NULL,
    event_type TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    unit TEXT NOT NULL,
    actor TEXT NOT NULL,
    metadata_json TEXT NOT NULL,
    created_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS billing_audit_events (
    id TEXT PRIMARY KEY,
    org_id TEXT NOT NULL,
    actor TEXT NOT NULL,
    action TEXT NOT NULL,
    target TEXT NOT NULL,
    payload_json TEXT NOT NULL,
    created_at TEXT NOT NULL
);
"""


class UsageLedger:
    def __init__(self, db_path: str | Path = "data/billing-usage.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(self.db_path) as con:
            con.executescript(SCHEMA)

    def record_usage(
        self,
        org_id: str,
        workspace_id: str,
        event_type: str,
        quantity: int = 1,
        unit: str = "count",
        actor: str = "system",
        metadata: dict | None = None,
    ) -> UsageEvent:
        event = UsageEvent(
            id=f"use_{uuid.uuid4().hex[:12]}",
            org_id=org_id,
            workspace_id=workspace_id,
            event_type=event_type,
            quantity=quantity,
            unit=unit,
            actor=actor,
            metadata=metadata or {},
        )
        issues = event.validate()
        if issues:
            raise ValueError("; ".join(issues))
        with sqlite3.connect(self.db_path) as con:
            con.execute(
                """
                INSERT INTO usage_events
                (id, org_id, workspace_id, event_type, quantity, unit, actor, metadata_json, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (event.id, event.org_id, event.workspace_id, event.event_type, event.quantity, event.unit, event.actor, json.dumps(event.metadata, sort_keys=True), event.created_at),
            )
        return event

    def list_usage(self, org_id: str, workspace_id: str | None = None, limit: int = 100) -> list[dict]:
        with sqlite3.connect(self.db_path) as con:
            if workspace_id:
                rows = con.execute(
                    """
                    SELECT id, org_id, workspace_id, event_type, quantity, unit, actor, metadata_json, created_at
                    FROM usage_events WHERE org_id=? AND workspace_id=?
                    ORDER BY created_at DESC LIMIT ?
                    """,
                    (org_id, workspace_id, limit),
                ).fetchall()
            else:
                rows = con.execute(
                    """
                    SELECT id, org_id, workspace_id, event_type, quantity, unit, actor, metadata_json, created_at
                    FROM usage_events WHERE org_id=?
                    ORDER BY created_at DESC LIMIT ?
                    """,
                    (org_id, limit),
                ).fetchall()
        return [
            {"id": r[0], "org_id": r[1], "workspace_id": r[2], "event_type": r[3], "quantity": r[4], "unit": r[5], "actor": r[6], "metadata": json.loads(r[7]), "created_at": r[8]}
            for r in rows
        ]

    def record_audit(self, org_id: str, actor: str, action: str, target: str, payload: dict | None = None) -> BillingAuditEvent:
        event = BillingAuditEvent(f"bae_{uuid.uuid4().hex[:12]}", org_id, actor, action, target, payload or {})
        with sqlite3.connect(self.db_path) as con:
            con.execute(
                """
                INSERT INTO billing_audit_events
                (id, org_id, actor, action, target, payload_json, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (event.id, event.org_id, event.actor, event.action, event.target, json.dumps(event.payload, sort_keys=True), event.created_at),
            )
        return event

    def list_audit(self, org_id: str, limit: int = 100) -> list[dict]:
        with sqlite3.connect(self.db_path) as con:
            rows = con.execute(
                """
                SELECT id, org_id, actor, action, target, payload_json, created_at
                FROM billing_audit_events WHERE org_id=?
                ORDER BY created_at DESC LIMIT ?
                """,
                (org_id, limit),
            ).fetchall()
        return [
            {"id": r[0], "org_id": r[1], "actor": r[2], "action": r[3], "target": r[4], "payload": json.loads(r[5]), "created_at": r[6]}
            for r in rows
        ]
