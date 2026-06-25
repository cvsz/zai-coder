"""Local background worker queue.

Jobs are stored in SQLite. Execution is handler-based and local only.
"""

from __future__ import annotations

import json
import sqlite3
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, Dict, Optional


SCHEMA = """
CREATE TABLE IF NOT EXISTS worker_jobs (
    id TEXT PRIMARY KEY,
    job_type TEXT NOT NULL,
    payload_json TEXT NOT NULL,
    status TEXT NOT NULL,
    result_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    started_at TEXT,
    completed_at TEXT
);
"""


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class WorkerJob:
    id: str
    job_type: str
    payload: dict
    status: str = "queued"
    result: dict = field(default_factory=dict)
    created_at: str = field(default_factory=now_iso)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "job_type": self.job_type,
            "payload": dict(self.payload),
            "status": self.status,
            "result": dict(self.result),
            "created_at": self.created_at,
        }


class WorkerQueue:
    def __init__(self, db_path: str | Path):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.handlers: Dict[str, Callable[[dict], dict]] = {}
        with sqlite3.connect(self.db_path) as con:
            con.executescript(SCHEMA)

    def register_handler(self, job_type: str, handler: Callable[[dict], dict]) -> None:
        self.handlers[job_type] = handler

    def enqueue(self, job_type: str, payload: dict) -> WorkerJob:
        job = WorkerJob(id=str(uuid.uuid4()), job_type=job_type, payload=payload)
        with sqlite3.connect(self.db_path) as con:
            con.execute(
                """
                INSERT INTO worker_jobs
                (id, job_type, payload_json, status, result_json, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (job.id, job.job_type, json.dumps(job.payload), job.status, json.dumps(job.result), job.created_at),
            )
        return job

    def run_one(self) -> Optional[WorkerJob]:
        with sqlite3.connect(self.db_path) as con:
            row = con.execute(
                "SELECT id, job_type, payload_json, status, result_json, created_at FROM worker_jobs WHERE status = 'queued' ORDER BY created_at LIMIT 1"
            ).fetchone()
            if not row:
                return None
            job_id, job_type, payload_json, *_ = row
            handler = self.handlers.get(job_type)
            if not handler:
                result = {"error": f"no handler for job type: {job_type}"}
                status = "failed"
            else:
                con.execute("UPDATE worker_jobs SET status = 'running', started_at = ? WHERE id = ?", (now_iso(), job_id))
                try:
                    result = handler(json.loads(payload_json))
                    status = "completed"
                except Exception as exc:  # defensive worker boundary
                    result = {"error": str(exc)}
                    status = "failed"
            con.execute(
                "UPDATE worker_jobs SET status = ?, result_json = ?, completed_at = ? WHERE id = ?",
                (status, json.dumps(result), now_iso(), job_id),
            )
            return WorkerJob(id=job_id, job_type=job_type, payload=json.loads(payload_json), status=status, result=result)
