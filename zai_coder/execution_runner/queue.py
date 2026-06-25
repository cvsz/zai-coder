"""Provider operation execution queue."""

from __future__ import annotations

import json
import sqlite3
import uuid
from pathlib import Path

from .models import CommandSpec, QueueItem

SCHEMA = """
CREATE TABLE IF NOT EXISTS execution_queue (
    id TEXT PRIMARY KEY,
    provider TEXT NOT NULL,
    action TEXT NOT NULL,
    command_json TEXT NOT NULL,
    status TEXT NOT NULL,
    attempts INTEGER NOT NULL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
"""


class ExecutionQueue:
    def __init__(self, db_path: str | Path = "data/execution-queue.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(self.db_path) as con:
            con.executescript(SCHEMA)

    def enqueue(self, provider: str, action: str, command: CommandSpec) -> QueueItem:
        item = QueueItem(id=str(uuid.uuid4()), provider=provider, action=action, command=command)
        with sqlite3.connect(self.db_path) as con:
            con.execute(
                """
                INSERT INTO execution_queue
                (id, provider, action, command_json, status, attempts)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (item.id, item.provider, item.action, json.dumps(command.to_dict(), sort_keys=True), item.status, item.attempts),
            )
        return item

    def next_item(self) -> QueueItem | None:
        with sqlite3.connect(self.db_path) as con:
            row = con.execute(
                """
                SELECT id, provider, action, command_json, status, attempts, created_at
                FROM execution_queue
                WHERE status = 'queued'
                ORDER BY created_at ASC
                LIMIT 1
                """
            ).fetchone()
        if not row:
            return None
        cmd_data = json.loads(row[3])
        command = CommandSpec(
            command=tuple(cmd_data["command"]),
            cwd=cmd_data["cwd"],
            timeout_seconds=cmd_data["timeout_seconds"],
            env_overlay={},
            apply=cmd_data["apply"],
            approval_id=cmd_data["approval_id"],
        )
        return QueueItem(id=row[0], provider=row[1], action=row[2], command=command, status=row[4], attempts=row[5], created_at=row[6])

    def mark_status(self, item_id: str, status: str, attempts: int | None = None) -> None:
        if status not in {"queued", "running", "completed", "failed", "blocked", "cancelled"}:
            raise ValueError(f"invalid status: {status}")
        with sqlite3.connect(self.db_path) as con:
            if attempts is None:
                con.execute("UPDATE execution_queue SET status = ? WHERE id = ?", (status, item_id))
            else:
                con.execute("UPDATE execution_queue SET status = ?, attempts = ? WHERE id = ?", (status, attempts, item_id))
