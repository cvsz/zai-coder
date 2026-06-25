"""Local portal inbox for notification drafts."""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path

from .models import CommunicationThread


SCHEMA = """
CREATE TABLE IF NOT EXISTS portal_inbox (
    id TEXT PRIMARY KEY,
    customer_id TEXT NOT NULL,
    subject TEXT NOT NULL,
    body TEXT NOT NULL,
    status TEXT NOT NULL,
    payload_json TEXT NOT NULL,
    created_at TEXT NOT NULL
);
"""


class PortalInbox:
    def __init__(self, db_path: str | Path = "data/notification-center.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(self.db_path) as con:
            con.executescript(SCHEMA)

    def store_draft(self, draft: dict, customer_id: str) -> dict:
        with sqlite3.connect(self.db_path) as con:
            con.execute(
                """
                INSERT INTO portal_inbox
                (id, customer_id, subject, body, status, payload_json, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (draft["id"], customer_id, draft["subject"], draft["body"], "draft", json.dumps(draft, sort_keys=True), draft["created_at"]),
            )
        return {"stored": True, "draft_id": draft["id"], "customer_id": customer_id}

    def list_drafts(self, customer_id: str | None = None) -> list[dict]:
        with sqlite3.connect(self.db_path) as con:
            if customer_id:
                rows = con.execute(
                    """
                    SELECT id, customer_id, subject, body, status, payload_json, created_at
                    FROM portal_inbox WHERE customer_id=? ORDER BY created_at DESC
                    """,
                    (customer_id,),
                ).fetchall()
            else:
                rows = con.execute(
                    """
                    SELECT id, customer_id, subject, body, status, payload_json, created_at
                    FROM portal_inbox ORDER BY created_at DESC
                    """
                ).fetchall()
        return [
            {"id": r[0], "customer_id": r[1], "subject": r[2], "body": r[3], "status": r[4], "payload": json.loads(r[5]), "created_at": r[6]}
            for r in rows
        ]


def thread_from_drafts(customer_id: str, subject: str, drafts: list[dict]) -> CommunicationThread:
    thread = CommunicationThread(
        id=f"thread_{customer_id}_{len(drafts)}",
        customer_id=customer_id,
        subject=subject,
        messages=tuple({"subject": draft["subject"], "body": draft["body"], "channel": draft["channel"]} for draft in drafts),
    )
    issues = thread.validate()
    if issues:
        raise ValueError("; ".join(issues))
    return thread
