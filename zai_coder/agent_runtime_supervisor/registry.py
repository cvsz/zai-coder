"""Agent runtime registry."""

from __future__ import annotations

import sqlite3
import uuid
from pathlib import Path

from .models import AgentRuntime, now_iso


SCHEMA = """
CREATE TABLE IF NOT EXISTS agent_runtimes (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    agent_type TEXT NOT NULL,
    org_id TEXT NOT NULL,
    workspace_id TEXT NOT NULL,
    status TEXT NOT NULL,
    model TEXT NOT NULL,
    worker_queue TEXT NOT NULL,
    heartbeat_at TEXT NOT NULL,
    created_at TEXT NOT NULL
);
"""


class AgentRegistry:
    def __init__(self, db_path: str | Path = "data/agent-runtime-supervisor.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(self.db_path) as con:
            con.executescript(SCHEMA)

    def register(self, name: str, agent_type: str, org_id: str, workspace_id: str, model: str = "local/mock-agent", worker_queue: str = "agents") -> AgentRuntime:
        agent = AgentRuntime(
            id=f"agent_{uuid.uuid4().hex[:12]}",
            name=name,
            agent_type=agent_type,
            org_id=org_id,
            workspace_id=workspace_id,
            model=model,
            worker_queue=worker_queue,
        )
        issues = agent.validate()
        if issues:
            raise ValueError("; ".join(issues))
        with sqlite3.connect(self.db_path) as con:
            con.execute(
                """
                INSERT INTO agent_runtimes
                (id, name, agent_type, org_id, workspace_id, status, model, worker_queue, heartbeat_at, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (agent.id, agent.name, agent.agent_type, agent.org_id, agent.workspace_id, agent.status, agent.model, agent.worker_queue, agent.heartbeat_at, agent.created_at),
            )
        return agent

    def update_status(self, agent_id: str, status: str) -> AgentRuntime | None:
        heartbeat = now_iso()
        with sqlite3.connect(self.db_path) as con:
            con.execute("UPDATE agent_runtimes SET status=?, heartbeat_at=? WHERE id=?", (status, heartbeat, agent_id))
            row = con.execute(
                """
                SELECT id, name, agent_type, org_id, workspace_id, status, model, worker_queue, heartbeat_at, created_at
                FROM agent_runtimes WHERE id=?
                """,
                (agent_id,),
            ).fetchone()
        if not row:
            return None
        return AgentRuntime(id=row[0], name=row[1], agent_type=row[2], org_id=row[3], workspace_id=row[4], status=row[5], model=row[6], worker_queue=row[7], heartbeat_at=row[8], created_at=row[9])

    def list_agents(self, org_id: str | None = None, workspace_id: str | None = None) -> list[dict]:
        query = """
            SELECT id, name, agent_type, org_id, workspace_id, status, model, worker_queue, heartbeat_at, created_at
            FROM agent_runtimes
        """
        params: tuple = ()
        if org_id and workspace_id:
            query += " WHERE org_id=? AND workspace_id=?"
            params = (org_id, workspace_id)
        elif org_id:
            query += " WHERE org_id=?"
            params = (org_id,)
        query += " ORDER BY created_at DESC"
        with sqlite3.connect(self.db_path) as con:
            rows = con.execute(query, params).fetchall()
        return [
            AgentRuntime(id=r[0], name=r[1], agent_type=r[2], org_id=r[3], workspace_id=r[4], status=r[5], model=r[6], worker_queue=r[7], heartbeat_at=r[8], created_at=r[9]).to_dict()
            for r in rows
        ]
