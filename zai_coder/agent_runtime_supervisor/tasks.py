"""Agent task assignment."""

from __future__ import annotations

import json
import sqlite3
import uuid
from pathlib import Path

from .models import AgentTask


SCHEMA = """
CREATE TABLE IF NOT EXISTS agent_tasks (
    id TEXT PRIMARY KEY,
    agent_id TEXT NOT NULL,
    org_id TEXT NOT NULL,
    workspace_id TEXT NOT NULL,
    title TEXT NOT NULL,
    instruction TEXT NOT NULL,
    status TEXT NOT NULL,
    priority INTEGER NOT NULL,
    created_at TEXT NOT NULL
);
"""


class AgentTaskStore:
    def __init__(self, db_path: str | Path = "data/agent-runtime-supervisor.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(self.db_path) as con:
            con.executescript(SCHEMA)

    def create_task(self, agent_id: str, org_id: str, workspace_id: str, title: str, instruction: str, priority: int = 100) -> AgentTask:
        task = AgentTask(
            id=f"agtask_{uuid.uuid4().hex[:12]}",
            agent_id=agent_id,
            org_id=org_id,
            workspace_id=workspace_id,
            title=title,
            instruction=instruction,
            priority=priority,
        )
        issues = task.validate()
        if issues:
            raise ValueError("; ".join(issues))
        with sqlite3.connect(self.db_path) as con:
            con.execute(
                """
                INSERT INTO agent_tasks
                (id, agent_id, org_id, workspace_id, title, instruction, status, priority, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (task.id, task.agent_id, task.org_id, task.workspace_id, task.title, task.instruction, task.status, task.priority, task.created_at),
            )
        return task

    def assign_next(self, agent_id: str) -> AgentTask | None:
        with sqlite3.connect(self.db_path) as con:
            row = con.execute(
                """
                SELECT id, agent_id, org_id, workspace_id, title, instruction, status, priority, created_at
                FROM agent_tasks
                WHERE agent_id=? AND status='queued'
                ORDER BY priority ASC, created_at ASC
                LIMIT 1
                """,
                (agent_id,),
            ).fetchone()
            if not row:
                return None
            con.execute("UPDATE agent_tasks SET status='assigned' WHERE id=?", (row[0],))
        return AgentTask(id=row[0], agent_id=row[1], org_id=row[2], workspace_id=row[3], title=row[4], instruction=row[5], status="assigned", priority=row[7], created_at=row[8])

    def list_tasks(self, agent_id: str | None = None) -> list[dict]:
        with sqlite3.connect(self.db_path) as con:
            if agent_id:
                rows = con.execute(
                    """
                    SELECT id, agent_id, org_id, workspace_id, title, instruction, status, priority, created_at
                    FROM agent_tasks WHERE agent_id=? ORDER BY created_at DESC
                    """,
                    (agent_id,),
                ).fetchall()
            else:
                rows = con.execute(
                    """
                    SELECT id, agent_id, org_id, workspace_id, title, instruction, status, priority, created_at
                    FROM agent_tasks ORDER BY created_at DESC
                    """
                ).fetchall()
        return [
            AgentTask(id=r[0], agent_id=r[1], org_id=r[2], workspace_id=r[3], title=r[4], instruction=r[5], status=r[6], priority=r[7], created_at=r[8]).to_dict()
            for r in rows
        ]
