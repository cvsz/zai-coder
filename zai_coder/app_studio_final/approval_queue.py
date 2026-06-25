"""Integration execution approval queue."""

from __future__ import annotations

import json
import sqlite3
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path


SCHEMA = """
CREATE TABLE IF NOT EXISTS approval_queue_items (
    id TEXT PRIMARY KEY,
    provider TEXT NOT NULL,
    action TEXT NOT NULL,
    plan_json TEXT NOT NULL,
    status TEXT NOT NULL,
    requested_by TEXT NOT NULL,
    created_at TEXT NOT NULL,
    decided_at TEXT
);
"""


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass(frozen=True)
class ApprovalItem:
    id: str
    provider: str
    action: str
    plan_json: str
    status: str
    requested_by: str
    created_at: str = field(default_factory=now_iso)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "provider": self.provider,
            "action": self.action,
            "plan_json": self.plan_json,
            "status": self.status,
            "requested_by": self.requested_by,
            "created_at": self.created_at,
        }


class ApprovalQueue:
    def __init__(self, db_path: str | Path):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(self.db_path) as con:
            con.executescript(SCHEMA)

    def submit(self, provider: str, action: str, plan: dict, requested_by: str) -> ApprovalItem:
        item = ApprovalItem(
            id=str(uuid.uuid4()),
            provider=provider,
            action=action,
            plan_json=json.dumps(plan, sort_keys=True),
            status="pending",
            requested_by=requested_by,
        )
        with sqlite3.connect(self.db_path) as con:
            con.execute(
                """
                INSERT INTO approval_queue_items
                (id, provider, action, plan_json, status, requested_by, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (item.id, item.provider, item.action, item.plan_json, item.status, item.requested_by, item.created_at),
            )
        return item

    def decide(self, item_id: str, status: str) -> None:
        if status not in {"approved", "rejected", "cancelled"}:
            raise ValueError(f"invalid decision: {status}")
        with sqlite3.connect(self.db_path) as con:
            cur = con.execute(
                "UPDATE approval_queue_items SET status = ?, decided_at = ? WHERE id = ? AND status = 'pending'",
                (status, now_iso(), item_id),
            )
            if cur.rowcount != 1:
                raise ValueError(f"pending approval item not found: {item_id}")
