"""Billing event replay protection and sandbox event handling."""

from __future__ import annotations

import json
import sqlite3
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


SCHEMA = """
CREATE TABLE IF NOT EXISTS billing_events (
    id TEXT PRIMARY KEY,
    provider TEXT NOT NULL,
    provider_event_id TEXT NOT NULL UNIQUE,
    type TEXT NOT NULL,
    status TEXT NOT NULL,
    payload_json TEXT NOT NULL,
    created_at TEXT NOT NULL
);
"""


@dataclass
class BillingEvent:
    id: str
    provider: str
    provider_event_id: str
    type: str
    status: str = "received"
    payload_json: str = "{}"
    created_at: str = field(default_factory=now_iso)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "provider": self.provider,
            "provider_event_id": self.provider_event_id,
            "type": self.type,
            "status": self.status,
            "payload_json": self.payload_json,
            "created_at": self.created_at,
        }


class BillingEventStore:
    def __init__(self, db_path: str | Path):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(self.db_path) as con:
            con.executescript(SCHEMA)

    def record(self, provider: str, provider_event_id: str, event_type: str, payload: dict) -> BillingEvent:
        event = BillingEvent(
            id=str(uuid.uuid4()),
            provider=provider,
            provider_event_id=provider_event_id,
            type=event_type,
            payload_json=json.dumps(payload, sort_keys=True),
        )
        with sqlite3.connect(self.db_path) as con:
            con.execute(
                """
                INSERT INTO billing_events
                (id, provider, provider_event_id, type, status, payload_json, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    event.id,
                    event.provider,
                    event.provider_event_id,
                    event.type,
                    event.status,
                    event.payload_json,
                    event.created_at,
                ),
            )
        return event
