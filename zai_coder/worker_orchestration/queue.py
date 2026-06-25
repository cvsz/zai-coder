"""Worker job queue with lease support."""

from __future__ import annotations

import json
import sqlite3
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path

from .models import WorkerJob, now_iso


SCHEMA = """
CREATE TABLE IF NOT EXISTS worker_jobs (
    id TEXT PRIMARY KEY,
    queue TEXT NOT NULL,
    job_type TEXT NOT NULL,
    org_id TEXT NOT NULL,
    workspace_id TEXT NOT NULL,
    payload_json TEXT NOT NULL,
    status TEXT NOT NULL,
    priority INTEGER NOT NULL,
    attempts INTEGER NOT NULL,
    max_attempts INTEGER NOT NULL,
    lease_worker_id TEXT NOT NULL,
    lease_expires_at TEXT NOT NULL,
    created_at TEXT NOT NULL
);
"""


def lease_expiry(seconds: int = 300) -> str:
    return (datetime.now(timezone.utc) + timedelta(seconds=seconds)).isoformat()


class WorkerJobQueue:
    def __init__(self, db_path: str | Path = "data/worker-orchestration.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(self.db_path) as con:
            con.executescript(SCHEMA)

    def enqueue(self, queue: str, job_type: str, org_id: str, workspace_id: str, payload: dict | None = None, priority: int = 100, max_attempts: int = 3) -> WorkerJob:
        job = WorkerJob(
            id=f"job_{uuid.uuid4().hex[:12]}",
            queue=queue,
            job_type=job_type,
            org_id=org_id,
            workspace_id=workspace_id,
            payload=payload or {},
            priority=priority,
            max_attempts=max_attempts,
        )
        issues = job.validate()
        if issues:
            raise ValueError("; ".join(issues))
        with sqlite3.connect(self.db_path) as con:
            con.execute(
                """
                INSERT INTO worker_jobs
                (id, queue, job_type, org_id, workspace_id, payload_json, status, priority, attempts, max_attempts, lease_worker_id, lease_expires_at, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (job.id, job.queue, job.job_type, job.org_id, job.workspace_id, json.dumps(job.payload, sort_keys=True), job.status, job.priority, job.attempts, job.max_attempts, job.lease_worker_id, job.lease_expires_at, job.created_at),
            )
        return job

    def lease_next(self, queue: str, worker_id: str, lease_seconds: int = 300) -> WorkerJob | None:
        expires = lease_expiry(lease_seconds)
        with sqlite3.connect(self.db_path) as con:
            row = con.execute(
                """
                SELECT id, queue, job_type, org_id, workspace_id, payload_json, status, priority, attempts, max_attempts, lease_worker_id, lease_expires_at, created_at
                FROM worker_jobs
                WHERE queue=? AND status='queued'
                ORDER BY priority ASC, created_at ASC
                LIMIT 1
                """,
                (queue,),
            ).fetchone()
            if not row:
                return None
            con.execute(
                "UPDATE worker_jobs SET status='leased', lease_worker_id=?, lease_expires_at=?, attempts=attempts+1 WHERE id=?",
                (worker_id, expires, row[0]),
            )
        return WorkerJob(id=row[0], queue=row[1], job_type=row[2], org_id=row[3], workspace_id=row[4], payload=json.loads(row[5]), status="leased", priority=row[7], attempts=row[8]+1, max_attempts=row[9], lease_worker_id=worker_id, lease_expires_at=expires, created_at=row[12])

    def mark(self, job_id: str, status: str) -> None:
        if status not in {"queued", "leased", "running", "completed", "failed", "dead_letter", "cancelled"}:
            raise ValueError("invalid job status")
        with sqlite3.connect(self.db_path) as con:
            con.execute("UPDATE worker_jobs SET status=? WHERE id=?", (status, job_id))

    def list_jobs(self, status: str | None = None, limit: int = 100) -> list[dict]:
        with sqlite3.connect(self.db_path) as con:
            if status:
                rows = con.execute(
                    """
                    SELECT id, queue, job_type, org_id, workspace_id, payload_json, status, priority, attempts, max_attempts, lease_worker_id, lease_expires_at, created_at
                    FROM worker_jobs WHERE status=? ORDER BY created_at DESC LIMIT ?
                    """,
                    (status, limit),
                ).fetchall()
            else:
                rows = con.execute(
                    """
                    SELECT id, queue, job_type, org_id, workspace_id, payload_json, status, priority, attempts, max_attempts, lease_worker_id, lease_expires_at, created_at
                    FROM worker_jobs ORDER BY created_at DESC LIMIT ?
                    """,
                    (limit,),
                ).fetchall()
        return [
            WorkerJob(id=r[0], queue=r[1], job_type=r[2], org_id=r[3], workspace_id=r[4], payload=json.loads(r[5]), status=r[6], priority=r[7], attempts=r[8], max_attempts=r[9], lease_worker_id=r[10], lease_expires_at=r[11], created_at=r[12]).to_dict()
            for r in rows
        ]
