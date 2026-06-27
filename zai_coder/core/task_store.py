import sqlite3
import time
from pathlib import Path
from typing import Any, Dict, List

class TaskStore:
    def __init__(self, db_path: str | Path):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(str(self.db_path))
        self.conn.row_factory = sqlite3.Row
        self._init_db()

    def _init_db(self):
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT,
                    agent TEXT,
                    prompt TEXT,
                    state TEXT,
                    created_at REAL,
                    updated_at REAL,
                    started_at REAL,
                    finished_at REAL,
                    error TEXT
                )
            """)
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS task_events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    task_id INTEGER,
                    event_type TEXT,
                    message TEXT,
                    created_at REAL,
                    FOREIGN KEY(task_id) REFERENCES tasks(id) ON DELETE CASCADE
                )
            """)
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS task_outputs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    task_id INTEGER,
                    role TEXT,
                    content TEXT,
                    created_at REAL,
                    FOREIGN KEY(task_id) REFERENCES tasks(id) ON DELETE CASCADE
                )
            """)

    def _task_dict(self, row: sqlite3.Row | None) -> Dict[str, Any] | None:
        if row is None:
            return None

        task = dict(row)
        # Keep legacy `state` and newer `status` consumers aligned without
        # changing the SQLite schema.
        if "state" in task and "status" not in task:
            task["status"] = task["state"]
        if "status" in task and "state" not in task:
            task["state"] = task["status"]
        return task

    def create(
        self,
        title: str,
        agent: str = "planner",
        description: str = "",
        metadata: Dict[str, Any] | None = None,
        prompt: str | None = None,
    ) -> Dict[str, Any]:
        """Create a task with the newer self-queue-style API."""
        del metadata  # Reserved for future schema expansion.
        task_prompt = prompt if prompt is not None else description
        task_id = self.create_task(title, agent, task_prompt)
        task = self.get_task(task_id)
        if task is None:
            raise RuntimeError(f"created task {task_id} could not be loaded")
        return task

    def create_task(self, title: str, agent: str, prompt: str) -> int:
        now = time.time()
        with self.conn:
            cur = self.conn.execute("""
                INSERT INTO tasks (title, agent, prompt, state, created_at, updated_at)
                VALUES (?, ?, ?, 'queued', ?, ?)
            """, (title, agent, prompt, now, now))
            return cur.lastrowid

    def get_task(self, task_id: int) -> Dict[str, Any] | None:
        cur = self.conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
        return self._task_dict(cur.fetchone())

    def list_tasks(self) -> List[Dict[str, Any]]:
        cur = self.conn.execute("SELECT * FROM tasks ORDER BY created_at DESC")
        return [task for row in cur.fetchall() if (task := self._task_dict(row)) is not None]

    def update_status(self, task_id: int, status: str, last_error: str | None = None, **_: Any) -> None:
        """Alias for newer self-queue adapters."""
        self.update_task_state(task_id, status, error=last_error or "")

    def update_task_state(self, task_id: int, state: str, error: str = ""):
        now = time.time()
        with self.conn:
            if state == "running":
                self.conn.execute("UPDATE tasks SET state = ?, updated_at = ?, started_at = COALESCE(started_at, ?) WHERE id = ?",
                                  (state, now, now, task_id))
            elif state in ["completed", "failed", "cancelled"]:
                self.conn.execute("UPDATE tasks SET state = ?, updated_at = ?, finished_at = COALESCE(finished_at, ?), error = ? WHERE id = ?",
                                  (state, now, now, error, task_id))
            else:
                self.conn.execute("UPDATE tasks SET state = ?, updated_at = ? WHERE id = ?",
                                  (state, now, task_id))

    def add_event(self, task_id: int, event_type: str, message: str):
        now = time.time()
        with self.conn:
            self.conn.execute("""
                INSERT INTO task_events (task_id, event_type, message, created_at)
                VALUES (?, ?, ?, ?)
            """, (task_id, event_type, message, now))

    def append_event(self, task_id: int, event_type: str, message: str) -> None:
        """Alias for newer self-queue adapters."""
        self.add_event(task_id, event_type, message)

    def get_events(self, task_id: int) -> List[Dict[str, Any]]:
        cur = self.conn.execute("SELECT * FROM task_events WHERE task_id = ? ORDER BY created_at ASC", (task_id,))
        return [dict(row) for row in cur.fetchall()]

    def add_output(self, task_id: int, role: str, content: str):
        now = time.time()
        with self.conn:
            self.conn.execute("""
                INSERT INTO task_outputs (task_id, role, content, created_at)
                VALUES (?, ?, ?, ?)
            """, (task_id, role, content, now))

    def append_output(self, task_id: int, role: str, content: str) -> None:
        """Alias for newer self-queue adapters."""
        self.add_output(task_id, role, content)

    def get_outputs(self, task_id: int) -> List[Dict[str, Any]]:
        cur = self.conn.execute("SELECT * FROM task_outputs WHERE task_id = ? ORDER BY created_at ASC", (task_id,))
        return [dict(row) for row in cur.fetchall()]
