from __future__ import annotations

import json
import sqlite3
import time
from pathlib import Path
from typing import Any, Iterable

from .task_models import (
    TASK_SCHEMA_NAME,
    TASK_SCHEMA_VERSION,
    TASK_STATES,
    TaskEventRecord,
    TaskOutputRecord,
    TaskRecord,
    is_terminal_state,
    normalize_task_state,
)

TASK_TABLE_COLUMNS = {
    "id",
    "title",
    "agent",
    "prompt",
    "state",
    "status",
    "priority",
    "parent_id",
    "created_at",
    "updated_at",
    "started_at",
    "finished_at",
    "error",
    "attempt_count",
    "max_attempts",
    "lease_owner",
    "lease_expires_at",
}

_UNSET = object()


class TaskStore:
    def __init__(self, db_path: str | Path):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(str(self.db_path))
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("PRAGMA foreign_keys = ON")
        self._init_db()

    def _init_db(self) -> None:
        with self.conn:
            self.conn.execute(
                """
                CREATE TABLE IF NOT EXISTS schema_version (
                    name TEXT PRIMARY KEY,
                    version INTEGER NOT NULL,
                    updated_at REAL NOT NULL
                )
                """
            )
            self.conn.execute(
                """
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    agent TEXT NOT NULL,
                    prompt TEXT NOT NULL,
                    state TEXT NOT NULL,
                    status TEXT NOT NULL,
                    priority INTEGER NOT NULL DEFAULT 100,
                    parent_id INTEGER,
                    created_at REAL NOT NULL,
                    updated_at REAL NOT NULL,
                    started_at REAL,
                    finished_at REAL,
                    error TEXT,
                    attempt_count INTEGER NOT NULL DEFAULT 0,
                    max_attempts INTEGER NOT NULL DEFAULT 3,
                    lease_owner TEXT,
                    lease_expires_at REAL
                )
                """
            )
            self.conn.execute(
                """
                CREATE TABLE IF NOT EXISTS task_events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    task_id INTEGER NOT NULL,
                    event_type TEXT NOT NULL,
                    message TEXT NOT NULL,
                    created_at REAL NOT NULL,
                    FOREIGN KEY(task_id) REFERENCES tasks(id) ON DELETE CASCADE
                )
                """
            )
            self.conn.execute(
                """
                CREATE TABLE IF NOT EXISTS task_outputs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    task_id INTEGER NOT NULL,
                    role TEXT NOT NULL,
                    content TEXT NOT NULL,
                    created_at REAL NOT NULL,
                    FOREIGN KEY(task_id) REFERENCES tasks(id) ON DELETE CASCADE
                )
                """
            )
        self._migrate_task_table()
        self._set_schema_version(TASK_SCHEMA_VERSION)

    def _table_columns(self, table: str) -> set[str]:
        cur = self.conn.execute(f"PRAGMA table_info({table})")
        return {row[1] for row in cur.fetchall()}

    def _migrate_task_table(self) -> None:
        columns = self._table_columns("tasks")
        if not columns:
            return

        additions = {
            "status": "TEXT NOT NULL DEFAULT 'queued'",
            "priority": "INTEGER NOT NULL DEFAULT 100",
            "parent_id": "INTEGER",
            "started_at": "REAL",
            "finished_at": "REAL",
            "error": "TEXT",
            "attempt_count": "INTEGER NOT NULL DEFAULT 0",
            "max_attempts": "INTEGER NOT NULL DEFAULT 3",
            "lease_owner": "TEXT",
            "lease_expires_at": "REAL",
        }

        with self.conn:
            for column, ddl in additions.items():
                if column not in columns:
                    self.conn.execute(f"ALTER TABLE tasks ADD COLUMN {column} {ddl}")

            columns = self._table_columns("tasks")
            if "state" in columns and "status" in columns:
                self.conn.execute(
                    """
                    UPDATE tasks
                       SET status = COALESCE(NULLIF(status, ''), state),
                           state = COALESCE(NULLIF(state, ''), status)
                    """
                )
            elif "state" in columns and "status" not in columns:
                self.conn.execute("UPDATE tasks SET state = COALESCE(NULLIF(state, ''), 'queued')")
            elif "status" in columns and "state" not in columns:
                self.conn.execute("UPDATE tasks SET status = COALESCE(NULLIF(status, ''), 'queued')")

    def _set_schema_version(self, version: int) -> None:
        now = time.time()
        with self.conn:
            self.conn.execute(
                """
                INSERT INTO schema_version (name, version, updated_at)
                VALUES (?, ?, ?)
                ON CONFLICT(name) DO UPDATE SET version=excluded.version, updated_at=excluded.updated_at
                """,
                (TASK_SCHEMA_NAME, version, now),
            )

    def schema_version(self) -> dict[str, Any]:
        cur = self.conn.execute(
            "SELECT name, version, updated_at FROM schema_version WHERE name = ?",
            (TASK_SCHEMA_NAME,),
        )
        row = cur.fetchone()
        if row is None:
            return {"name": TASK_SCHEMA_NAME, "version": 0, "updated_at": None}
        return dict(row)

    def _task_row_to_record(self, row: sqlite3.Row | None) -> dict[str, Any] | None:
        if row is None:
            return None
        data = dict(row)
        try:
            data["state"] = normalize_task_state(data.get("state") or data.get("status") or "queued")
        except ValueError:
            data["state"] = "queued"
        try:
            data["status"] = normalize_task_state(data.get("status") or data.get("state") or "queued")
        except ValueError:
            data["status"] = data["state"]
        data["priority"] = int(data.get("priority", 100))
        data["attempt_count"] = int(data.get("attempt_count", 0))
        data["max_attempts"] = int(data.get("max_attempts", 3))
        data["error"] = data.get("error") or ""
        data["lease_owner"] = data.get("lease_owner") or ""
        return data

    def _row_to_event(self, row: sqlite3.Row) -> dict[str, Any]:
        return TaskEventRecord(
            id=row["id"],
            task_id=row["task_id"],
            event_type=row["event_type"],
            message=row["message"],
            created_at=row["created_at"],
        ).to_dict()

    def _row_to_output(self, row: sqlite3.Row) -> dict[str, Any]:
        return TaskOutputRecord(
            id=row["id"],
            task_id=row["task_id"],
            role=row["role"],
            content=row["content"],
            created_at=row["created_at"],
        ).to_dict()

    def create(
        self,
        title: str,
        agent: str = "planner",
        description: str = "",
        metadata: dict[str, Any] | None = None,
        prompt: str | None = None,
        *,
        priority: int = 100,
        parent_id: int | None = None,
        max_attempts: int = 3,
    ) -> dict[str, Any]:
        del metadata
        task_id = self.create_task(
            title=title,
            agent=agent,
            prompt=prompt if prompt is not None else description,
            priority=priority,
            parent_id=parent_id,
            max_attempts=max_attempts,
        )
        task = self.get_task(task_id)
        if task is None:
            raise RuntimeError(f"created task {task_id} could not be loaded")
        return task

    def create_task(
        self,
        title: str,
        agent: str,
        prompt: str,
        *,
        priority: int = 100,
        parent_id: int | None = None,
        max_attempts: int = 3,
    ) -> int:
        now = time.time()
        state = "queued"
        with self.conn:
            cur = self.conn.execute(
                """
                INSERT INTO tasks (
                    title, agent, prompt, state, status, priority, parent_id,
                    created_at, updated_at, started_at, finished_at, error,
                    attempt_count, max_attempts, lease_owner, lease_expires_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, NULL, NULL, NULL, 0, ?, NULL, NULL)
                """,
                (title, agent, prompt, state, state, priority, parent_id, now, now, max_attempts),
            )
            return int(cur.lastrowid)

    def get_task(self, task_id: int) -> dict[str, Any] | None:
        cur = self.conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
        return self._task_row_to_record(cur.fetchone())

    def list_tasks(self) -> list[dict[str, Any]]:
        cur = self.conn.execute("SELECT * FROM tasks ORDER BY priority ASC, created_at DESC, id DESC")
        return [task for row in cur.fetchall() if (task := self._task_row_to_record(row)) is not None]

    def list_tasks_by_state(self, state: str) -> list[dict[str, Any]]:
        normalized = normalize_task_state(state)
        cur = self.conn.execute(
            "SELECT * FROM tasks WHERE state = ? OR status = ? ORDER BY priority ASC, created_at DESC, id DESC",
            (normalized, normalized),
        )
        return [task for row in cur.fetchall() if (task := self._task_row_to_record(row)) is not None]

    def update_status(self, task_id: int, status: str, last_error: str | None = None, **_: Any) -> None:
        self.update_task_state(task_id, status, error=last_error or "")

    def update_task(
        self,
        task_id: int,
        *,
        state: str | object = _UNSET,
        title: str | object = _UNSET,
        agent: str | object = _UNSET,
        prompt: str | object = _UNSET,
        priority: int | object = _UNSET,
        parent_id: int | None | object = _UNSET,
        started_at: float | None | object = _UNSET,
        finished_at: float | None | object = _UNSET,
        error: str | None | object = _UNSET,
        attempt_count: int | object = _UNSET,
        max_attempts: int | object = _UNSET,
        lease_owner: str | None | object = _UNSET,
        lease_expires_at: float | None | object = _UNSET,
    ) -> None:
        now = time.time()
        updates: list[str] = []
        values: list[Any] = []

        if state is not _UNSET:
            normalized = normalize_task_state(state)
            updates.append("state = ?")
            values.append(normalized)
            updates.append("status = ?")
            values.append(normalized)
        if title is not _UNSET:
            updates.append("title = ?")
            values.append(title)
        if agent is not _UNSET:
            updates.append("agent = ?")
            values.append(agent)
        if prompt is not _UNSET:
            updates.append("prompt = ?")
            values.append(prompt)
        if priority is not _UNSET:
            updates.append("priority = ?")
            values.append(priority)
        if parent_id is not _UNSET:
            updates.append("parent_id = ?")
            values.append(parent_id)
        if started_at is not _UNSET:
            updates.append("started_at = ?")
            values.append(started_at)
        if finished_at is not _UNSET:
            updates.append("finished_at = ?")
            values.append(finished_at)
        if error is not _UNSET:
            updates.append("error = ?")
            values.append(error)
        if attempt_count is not _UNSET:
            updates.append("attempt_count = ?")
            values.append(attempt_count)
        if max_attempts is not _UNSET:
            updates.append("max_attempts = ?")
            values.append(max_attempts)
        if lease_owner is not _UNSET:
            updates.append("lease_owner = ?")
            values.append(lease_owner)
        if lease_expires_at is not _UNSET:
            updates.append("lease_expires_at = ?")
            values.append(lease_expires_at)

        updates.append("updated_at = ?")
        values.append(now)
        values.append(task_id)

        with self.conn:
            self.conn.execute(f"UPDATE tasks SET {', '.join(updates)} WHERE id = ?", values)

    def update_task_state(self, task_id: int, state: str, error: str = "") -> None:
        normalized = normalize_task_state(state)
        now = time.time()
        updates: list[str] = ["state = ?", "status = ?", "updated_at = ?"]
        values: list[Any] = [normalized, normalized, now]

        if normalized == "running":
            updates.append("started_at = COALESCE(started_at, ?)")
            values.append(now)
        elif normalized in {"completed", "failed", "cancelled"}:
            updates.append("finished_at = COALESCE(finished_at, ?)")
            values.append(now)
            updates.append("error = ?")
            values.append(error)
            updates.append("lease_owner = NULL")
            updates.append("lease_expires_at = NULL")
        elif normalized == "queued":
            updates.append("lease_owner = NULL")
            updates.append("lease_expires_at = NULL")
        elif normalized == "waiting_approval":
            updates.append("lease_expires_at = NULL")

        values.append(task_id)
        with self.conn:
            self.conn.execute(f"UPDATE tasks SET {', '.join(updates)} WHERE id = ?", values)

    def cancel_task(self, task_id: int, message: str = "Task cancelled.") -> dict[str, Any] | None:
        task = self.get_task(task_id)
        if task is None:
            return None
        if is_terminal_state(task["state"]):
            return task
        self.update_task_state(task_id, "cancelled")
        self.add_event(task_id, "cancel", message)
        return self.get_task(task_id)

    def retry_task(self, task_id: int) -> dict[str, Any] | None:
        task = self.get_task(task_id)
        if task is None:
            return None
        if task["state"] == "running":
            raise ValueError("Cannot retry a running task")
        self.update_task(
            task_id,
            state="queued",
            error="",
            lease_owner=None,
            lease_expires_at=None,
            finished_at=None,
        )
        self.add_event(task_id, "retry", "Task returned to queued state.")
        return self.get_task(task_id)

    def claim_next_task(self, worker_id: str, lease_seconds: int = 300) -> dict[str, Any] | None:
        self.release_expired_leases()
        now = time.time()
        expires_at = now + max(1, int(lease_seconds))
        with self.conn:
            row = self.conn.execute(
                """
                SELECT *
                  FROM tasks
                 WHERE state = 'queued'
                 ORDER BY priority ASC, created_at ASC, id ASC
                 LIMIT 1
                """
            ).fetchone()
            if row is None:
                return None
            task_id = int(row["id"])
            self.conn.execute(
                """
                UPDATE tasks
                   SET state = 'running',
                       status = 'running',
                       attempt_count = attempt_count + 1,
                       lease_owner = ?,
                       lease_expires_at = ?,
                       started_at = COALESCE(started_at, ?),
                       updated_at = ?
                 WHERE id = ?
                """,
                (worker_id, expires_at, now, now, task_id),
            )
        self.add_event(task_id, "lease", f"Task leased by {worker_id}.")
        return self.get_task(task_id)

    def release_expired_leases(self) -> int:
        now = time.time()
        with self.conn:
            cur = self.conn.execute(
                """
                UPDATE tasks
                   SET state = 'queued',
                       status = 'queued',
                       lease_owner = NULL,
                       lease_expires_at = NULL,
                       updated_at = ?
                 WHERE state = 'running'
                   AND lease_expires_at IS NOT NULL
                   AND lease_expires_at < ?
                """,
                (now, now),
            )
        return cur.rowcount

    def add_event(self, task_id: int, event_type: str, message: str) -> None:
        now = time.time()
        with self.conn:
            self.conn.execute(
                """
                INSERT INTO task_events (task_id, event_type, message, created_at)
                VALUES (?, ?, ?, ?)
                """,
                (task_id, event_type, message, now),
            )

    def append_event(self, task_id: int, event_type: str, message: str) -> None:
        self.add_event(task_id, event_type, message)

    def get_events(self, task_id: int) -> list[dict[str, Any]]:
        cur = self.conn.execute("SELECT * FROM task_events WHERE task_id = ? ORDER BY created_at ASC, id ASC", (task_id,))
        return [self._row_to_event(row) for row in cur.fetchall()]

    def add_output(self, task_id: int, role: str, content: str) -> None:
        now = time.time()
        with self.conn:
            self.conn.execute(
                """
                INSERT INTO task_outputs (task_id, role, content, created_at)
                VALUES (?, ?, ?, ?)
                """,
                (task_id, role, content, now),
            )

    def append_output(self, task_id: int, role: str, content: str) -> None:
        self.add_output(task_id, role, content)

    def get_outputs(self, task_id: int) -> list[dict[str, Any]]:
        cur = self.conn.execute("SELECT * FROM task_outputs WHERE task_id = ? ORDER BY created_at ASC, id ASC", (task_id,))
        return [self._row_to_output(row) for row in cur.fetchall()]

    def export_json(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version(),
            "tasks": self.list_tasks(),
            "events": self.get_all_events(),
            "outputs": self.get_all_outputs(),
        }

    def get_all_events(self) -> list[dict[str, Any]]:
        cur = self.conn.execute("SELECT * FROM task_events ORDER BY created_at ASC, id ASC")
        return [self._row_to_event(row) for row in cur.fetchall()]

    def get_all_outputs(self) -> list[dict[str, Any]]:
        cur = self.conn.execute("SELECT * FROM task_outputs ORDER BY created_at ASC, id ASC")
        return [self._row_to_output(row) for row in cur.fetchall()]
