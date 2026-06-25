"""SQLite execution journal."""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path

from .models import ExecutionResult, QueueItem

SCHEMA = """
CREATE TABLE IF NOT EXISTS execution_journal (
    id TEXT PRIMARY KEY,
    provider TEXT NOT NULL,
    action TEXT NOT NULL,
    status TEXT NOT NULL,
    dry_run INTEGER NOT NULL,
    returncode INTEGER,
    stdout TEXT NOT NULL,
    stderr TEXT NOT NULL,
    blocked_reasons_json TEXT NOT NULL,
    item_json TEXT NOT NULL,
    result_json TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
"""


class ExecutionJournal:
    def __init__(self, db_path: str | Path = "data/execution-journal.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(self.db_path) as con:
            con.executescript(SCHEMA)

    def record(self, item: QueueItem, result: ExecutionResult) -> str:
        with sqlite3.connect(self.db_path) as con:
            con.execute(
                """
                INSERT OR REPLACE INTO execution_journal
                (id, provider, action, status, dry_run, returncode, stdout, stderr, blocked_reasons_json, item_json, result_json)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    result.id,
                    item.provider,
                    item.action,
                    result.status,
                    int(result.dry_run),
                    result.returncode,
                    result.stdout,
                    result.stderr,
                    json.dumps(list(result.blocked_reasons)),
                    json.dumps(item.to_dict(), sort_keys=True),
                    json.dumps(result.to_dict(), sort_keys=True),
                ),
            )
        return result.id

    def list_events(self, limit: int = 50) -> list[dict]:
        with sqlite3.connect(self.db_path) as con:
            rows = con.execute(
                """
                SELECT id, provider, action, status, dry_run, returncode, stdout, stderr, blocked_reasons_json, created_at
                FROM execution_journal
                ORDER BY created_at DESC
                LIMIT ?
                """,
                (limit,),
            ).fetchall()
        return [
            {
                "id": row[0],
                "provider": row[1],
                "action": row[2],
                "status": row[3],
                "dry_run": bool(row[4]),
                "returncode": row[5],
                "stdout": row[6],
                "stderr": row[7],
                "blocked_reasons": json.loads(row[8]),
                "created_at": row[9],
            }
            for row in rows
        ]
