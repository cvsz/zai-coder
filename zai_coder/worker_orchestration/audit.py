"""Worker event/audit log."""

from __future__ import annotations

import json
import sqlite3
import uuid
from pathlib import Path

from .models import WorkerEvent


SCHEMA = """
CREATE TABLE IF NOT EXISTS worker_events (
    id TEXT PRIMARY KEY,
    worker_id TEXT NOT NULL,
    job_id TEXT NOT NULL,
    event_type TEXT NOT NULL,
    message TEXT NOT NULL,
    payload_json TEXT NOT NULL,
    created_at TEXT NOT NULL
);
"""


class WorkerAuditLog:
    def __init__(self, db_path: str | Path = "data/worker-orchestration.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(self.db_path) as con:
            con.executescript(SCHEMA)

    def record(self, worker_id: str, job_id: str, event_type: str, message: str, payload: dict | None = None) -> WorkerEvent:
        event = WorkerEvent(f"wev_{uuid.uuid4().hex[:12]}", worker_id, job_id, event_type, message, payload or {})
        with sqlite3.connect(self.db_path) as con:
            con.execute(
                """
                INSERT INTO worker_events
                (id, worker_id, job_id, event_type, message, payload_json, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (event.id, event.worker_id, event.job_id, event.event_type, event.message, json.dumps(event.payload, sort_keys=True), event.created_at),
            )
        return event

    def list_events(self, limit: int = 100) -> list[dict]:
        with sqlite3.connect(self.db_path) as con:
            rows = con.execute(
                """
                SELECT id, worker_id, job_id, event_type, message, payload_json, created_at
                FROM worker_events ORDER BY created_at DESC LIMIT ?
                """,
                (limit,),
            ).fetchall()
        return [
            {"id": r[0], "worker_id": r[1], "job_id": r[2], "event_type": r[3], "message": r[4], "payload": json.loads(r[5]), "created_at": r[6]}
            for r in rows
        ]
