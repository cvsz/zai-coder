from __future__ import annotations

import json
import sqlite3
import time
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any

@dataclass
class ScheduledJob:
    id: int
    name: str
    command: str
    schedule: str
    enabled: bool
    profile: str
    created_at: float
    last_run_at: float | None
    last_result: str | None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

class LocalScheduler:
    def __init__(self, db_path: str | Path):
        self.db_path = Path(db_path).expanduser().resolve()
        self._init_db()

    def _init_db(self):
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS scheduled_jobs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    command TEXT NOT NULL,
                    schedule TEXT NOT NULL,
                    enabled BOOLEAN NOT NULL DEFAULT 0,
                    profile TEXT NOT NULL,
                    created_at REAL NOT NULL,
                    last_run_at REAL,
                    last_result TEXT
                )
                """
            )
            conn.commit()

    def add_job(self, name: str, command: str, schedule: str, profile: str = "default", enabled: bool = False) -> int:
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.execute(
                """
                INSERT INTO scheduled_jobs (name, command, schedule, enabled, profile, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (name, command, schedule, int(enabled), profile, time.time())
            )
            conn.commit()
            return cur.lastrowid

    def list_jobs(self) -> list[ScheduledJob]:
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.execute("SELECT * FROM scheduled_jobs ORDER BY id ASC")
            return [
                ScheduledJob(
                    id=row["id"],
                    name=row["name"],
                    command=row["command"],
                    schedule=row["schedule"],
                    enabled=bool(row["enabled"]),
                    profile=row["profile"],
                    created_at=row["created_at"],
                    last_run_at=row["last_run_at"],
                    last_result=row["last_result"]
                )
                for row in cur.fetchall()
            ]

    def set_enabled(self, job_id: int, enabled: bool):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("UPDATE scheduled_jobs SET enabled = ? WHERE id = ?", (int(enabled), job_id))
            conn.commit()

    def delete_job(self, job_id: int):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("DELETE FROM scheduled_jobs WHERE id = ?", (job_id,))
            conn.commit()

    def run_job_dry_run(self, job_id: int) -> dict[str, Any]:
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.execute("SELECT * FROM scheduled_jobs WHERE id = ?", (job_id,))
            row = cur.fetchone()
            if not row:
                raise ValueError(f"Job {job_id} not found")
            
            return {
                "job_id": row["id"],
                "name": row["name"],
                "command": row["command"],
                "dry_run": True,
                "status": "simulated",
                "message": f"Would execute command: {row['command']} with profile {row['profile']}"
            }

    def get_pending_jobs(self) -> list[ScheduledJob]:
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.execute("SELECT * FROM scheduled_jobs WHERE enabled = 1 ORDER BY id ASC")
            # In a real scheduler we would parse the 'schedule' (cron or interval) to check if it's due.
            # For this foundation, we just return all enabled jobs.
            return [
                ScheduledJob(
                    id=row["id"],
                    name=row["name"],
                    command=row["command"],
                    schedule=row["schedule"],
                    enabled=bool(row["enabled"]),
                    profile=row["profile"],
                    created_at=row["created_at"],
                    last_run_at=row["last_run_at"],
                    last_result=row["last_result"]
                )
                for row in cur.fetchall()
            ]

    def update_job_status(self, job_id: int, result: str):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "UPDATE scheduled_jobs SET last_run_at = ?, last_result = ? WHERE id = ?",
                (time.time(), result, job_id)
            )
            conn.commit()

    def process_pending_jobs(self, callback: Any) -> int:
        """
        Polls for pending jobs, executes them via callback, and updates their status.
        Returns the number of jobs processed.
        """
        jobs = self.get_pending_jobs()
        processed = 0
        for job in jobs:
            try:
                # Basic check if it's due could be added here if 'schedule' was parsed.
                # Currently we execute all enabled pending.
                result = callback(job)
                self.update_job_status(job.id, str(result))
                processed += 1
            except Exception as e:
                self.update_job_status(job.id, f"Error: {e}")
        return processed
