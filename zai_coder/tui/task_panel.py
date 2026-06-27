from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any


class TaskPanelAdapter:
    def __init__(self, workspace: str | Path):
        self.workspace = Path(workspace).expanduser().resolve()
        self.db_path = self.workspace / ".zai-coder" / "tasks" / "tasks.db"

    def exists(self) -> bool:
        return self.db_path.exists()

    def _query(self, sql: str, params: tuple[Any, ...] = ()) -> list[dict[str, Any]]:
        if not self.exists():
            return []
        with sqlite3.connect(f"file:{self.db_path}?mode=ro", uri=True) as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.execute(sql, params)
            return [dict(row) for row in cur.fetchall()]

    def _columns(self) -> set[str]:
        """Return the set of column names in the tasks table."""
        if not self.exists():
            return set()
        with sqlite3.connect(f"file:{self.db_path}?mode=ro", uri=True) as conn:
            cur = conn.execute("PRAGMA table_info(tasks)")
            return {row[1] for row in cur.fetchall()}

    def summary(self, limit: int = 5) -> dict[str, Any]:
        if not self.exists():
            return {"available": False, "count": 0, "queued": 0, "running": 0, "completed": 0, "failed": 0, "cancelled": 0, "items": []}

        cols = self._columns()
        state_expr = (
            "CASE WHEN state IS NOT NULL AND state != '' THEN state ELSE 'queued' END"
        )
        # Build SELECT list from available columns only
        select_parts = ["id", "title", "agent", f"{state_expr} AS state"]
        if "priority" in cols:
            select_parts.append("priority")
        else:
            select_parts.append("100 AS priority")
        if "updated_at" in cols:
            select_parts.append("updated_at")

        order_by = "priority ASC, created_at DESC, id DESC" if "priority" in cols else "created_at DESC, id DESC"

        rows = self._query(
            f"""
            SELECT {', '.join(select_parts)}
              FROM tasks
             ORDER BY {order_by}
             LIMIT ?
            """,
            (limit,),
        )
        counts = self._query(
            f"""
            SELECT {state_expr} AS state, COUNT(*) AS count
              FROM tasks
             GROUP BY {state_expr}
            """
        )
        state_counts = {row["state"]: row["count"] for row in counts}
        return {
            "available": True,
            "count": sum(state_counts.values()),
            "queued": state_counts.get("queued", 0),
            "running": state_counts.get("running", 0),
            "completed": state_counts.get("completed", 0),
            "failed": state_counts.get("failed", 0),
            "cancelled": state_counts.get("cancelled", 0),
            "items": rows,
        }

    def render(self, limit: int = 5) -> str:
        if not self.exists():
            return "Task DB not initialized."

        payload = self.summary(limit=limit)
        if payload["count"] == 0:
            return "No tasks."

        header = (
            f"Tasks: {payload['count']} total | queued={payload['queued']} "
            f"running={payload['running']} completed={payload['completed']} "
            f"failed={payload['failed']} cancelled={payload['cancelled']}"
        )
        items = [
            f"[{row['id']}] {row['state'].upper()}: {row['title']} (agent: {row['agent']}, priority: {row['priority']})"
            for row in payload["items"]
        ]
        return "\n".join([header, *items])


    def chip(self, limit: int = 5) -> str:
        payload = self.summary(limit=limit)
        if not payload["available"]:
            return "Task DB not initialized."
        if payload["count"] == 0:
            return "No tasks."
        return f"{payload['queued']} queued, {payload['running']} running, {payload['completed']} done"


TaskPanel = TaskPanelAdapter

