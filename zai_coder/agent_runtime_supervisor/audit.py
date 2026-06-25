"""Agent audit log."""

from __future__ import annotations

import json
import sqlite3
import uuid
from pathlib import Path

from .models import AgentAuditEvent


SCHEMA = """
CREATE TABLE IF NOT EXISTS agent_audit_events (
    id TEXT PRIMARY KEY,
    agent_id TEXT NOT NULL,
    org_id TEXT NOT NULL,
    workspace_id TEXT NOT NULL,
    actor TEXT NOT NULL,
    action TEXT NOT NULL,
    target TEXT NOT NULL,
    payload_json TEXT NOT NULL,
    created_at TEXT NOT NULL
);
"""


class AgentAuditLog:
    def __init__(self, db_path: str | Path = "data/agent-runtime-supervisor.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(self.db_path) as con:
            con.executescript(SCHEMA)

    def record(self, agent_id: str, org_id: str, workspace_id: str, actor: str, action: str, target: str, payload: dict | None = None) -> AgentAuditEvent:
        event = AgentAuditEvent(f"aae_{uuid.uuid4().hex[:12]}", agent_id, org_id, workspace_id, actor, action, target, payload or {})
        with sqlite3.connect(self.db_path) as con:
            con.execute(
                """
                INSERT INTO agent_audit_events
                (id, agent_id, org_id, workspace_id, actor, action, target, payload_json, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (event.id, event.agent_id, event.org_id, event.workspace_id, event.actor, event.action, event.target, json.dumps(event.payload, sort_keys=True), event.created_at),
            )
        return event

    def list_events(self, agent_id: str | None = None, limit: int = 100) -> list[dict]:
        with sqlite3.connect(self.db_path) as con:
            if agent_id:
                rows = con.execute(
                    """
                    SELECT id, agent_id, org_id, workspace_id, actor, action, target, payload_json, created_at
                    FROM agent_audit_events WHERE agent_id=? ORDER BY created_at DESC LIMIT ?
                    """,
                    (agent_id, limit),
                ).fetchall()
            else:
                rows = con.execute(
                    """
                    SELECT id, agent_id, org_id, workspace_id, actor, action, target, payload_json, created_at
                    FROM agent_audit_events ORDER BY created_at DESC LIMIT ?
                    """,
                    (limit,),
                ).fetchall()
        return [
            {"id": r[0], "agent_id": r[1], "org_id": r[2], "workspace_id": r[3], "actor": r[4], "action": r[5], "target": r[6], "payload": json.loads(r[7]), "created_at": r[8]}
            for r in rows
        ]
