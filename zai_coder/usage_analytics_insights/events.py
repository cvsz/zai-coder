"""Usage event ledger."""

from __future__ import annotations

import json
import sqlite3
import uuid
from pathlib import Path

from .models import UsageEvent
from .privacy import privacy_gate, redact_metadata


SCHEMA = """
CREATE TABLE IF NOT EXISTS usage_events (
    id TEXT PRIMARY KEY,
    event_type TEXT NOT NULL,
    customer_id TEXT NOT NULL,
    org_id TEXT NOT NULL,
    workspace_id TEXT NOT NULL,
    actor_id TEXT NOT NULL,
    feature_id TEXT NOT NULL,
    quantity REAL NOT NULL,
    metadata_json TEXT NOT NULL,
    created_at TEXT NOT NULL
);
"""


class UsageEventLedger:
    def __init__(self, db_path: str | Path = "data/usage-analytics.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(self.db_path) as con:
            con.executescript(SCHEMA)

    def record_event(
        self,
        event_type: str,
        customer_id: str,
        org_id: str,
        workspace_id: str,
        actor_id: str = "anonymous",
        feature_id: str = "unknown",
        quantity: float = 1.0,
        metadata: dict | None = None,
    ) -> UsageEvent:
        metadata = metadata or {}
        gate = privacy_gate({"metadata": metadata})
        if not gate["allowed"]:
            raise ValueError("; ".join(gate["blocked"]))
        event = UsageEvent(
            id=f"ue_{uuid.uuid4().hex[:12]}",
            event_type=event_type,
            customer_id=customer_id,
            org_id=org_id,
            workspace_id=workspace_id,
            actor_id=actor_id,
            feature_id=feature_id,
            quantity=quantity,
            metadata=redact_metadata(metadata),
        )
        issues = event.validate()
        if issues:
            raise ValueError("; ".join(issues))
        with sqlite3.connect(self.db_path) as con:
            con.execute(
                """
                INSERT INTO usage_events
                (id, event_type, customer_id, org_id, workspace_id, actor_id, feature_id, quantity, metadata_json, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (event.id, event.event_type, event.customer_id, event.org_id, event.workspace_id, event.actor_id, event.feature_id, event.quantity, json.dumps(event.metadata, sort_keys=True), event.created_at),
            )
        return event

    def list_events(self, customer_id: str | None = None, limit: int = 500) -> list[dict]:
        with sqlite3.connect(self.db_path) as con:
            if customer_id:
                rows = con.execute(
                    """
                    SELECT id, event_type, customer_id, org_id, workspace_id, actor_id, feature_id, quantity, metadata_json, created_at
                    FROM usage_events WHERE customer_id=? ORDER BY created_at DESC LIMIT ?
                    """,
                    (customer_id, limit),
                ).fetchall()
            else:
                rows = con.execute(
                    """
                    SELECT id, event_type, customer_id, org_id, workspace_id, actor_id, feature_id, quantity, metadata_json, created_at
                    FROM usage_events ORDER BY created_at DESC LIMIT ?
                    """,
                    (limit,),
                ).fetchall()
        return [
            {
                "id": r[0],
                "event_type": r[1],
                "customer_id": r[2],
                "org_id": r[3],
                "workspace_id": r[4],
                "actor_id": r[5],
                "feature_id": r[6],
                "quantity": r[7],
                "metadata": json.loads(r[8]),
                "created_at": r[9],
            }
            for r in rows
        ]


def seed_demo_events(db_path: str | Path = "data/usage-analytics.db") -> list[dict]:
    ledger = UsageEventLedger(db_path)
    rows = [
        ledger.record_event("portal.view", "cust_demo", "org_demo", "ws_demo", "usr_demo", "dashboard", 1, {"source": "demo"}),
        ledger.record_event("onboarding.step", "cust_demo", "org_demo", "ws_demo", "usr_demo", "onboarding", 1, {"step": "welcome"}),
        ledger.record_event("support.ticket", "cust_demo", "org_demo", "ws_demo", "usr_demo", "support", 1, {"priority": "normal"}),
        ledger.record_event("feature.use", "cust_demo", "org_demo", "ws_demo", "usr_demo", "connectors", 3, {"connector": "github"}),
        ledger.record_event("feature.use", "cust_local", "org_local", "ws_default", "usr_admin", "admin", 5, {"scope": "admin"}),
    ]
    return [row.to_dict() for row in rows]
