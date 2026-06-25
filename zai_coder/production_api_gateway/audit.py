"""Gateway audit log."""

from __future__ import annotations

import json
import sqlite3
import uuid
from pathlib import Path

from .models import GatewayAuditEvent, GatewayRequest, GatewayResponse
from .tenant_context import extract_tenant_context


SCHEMA = """
CREATE TABLE IF NOT EXISTS gateway_audit_events (
    id TEXT PRIMARY KEY,
    actor TEXT NOT NULL,
    org_id TEXT NOT NULL,
    workspace_id TEXT NOT NULL,
    action TEXT NOT NULL,
    target TEXT NOT NULL,
    status INTEGER NOT NULL,
    payload_json TEXT NOT NULL,
    created_at TEXT NOT NULL
);
"""


class GatewayAuditLog:
    def __init__(self, db_path: str | Path = "data/gateway-audit.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(self.db_path) as con:
            con.executescript(SCHEMA)

    def record(self, request: GatewayRequest, response: GatewayResponse) -> GatewayAuditEvent:
        tenant = extract_tenant_context(request)
        event = GatewayAuditEvent(
            id=f"gae_{uuid.uuid4().hex[:12]}",
            actor=tenant.actor if tenant else "anonymous",
            org_id=tenant.org_id if tenant else "unknown",
            workspace_id=tenant.workspace_id if tenant else "unknown",
            action=f"{request.normalized_method()} {request.path}",
            target=request.path,
            status=response.status,
            payload={"request": request.to_safe_dict(), "response_status": response.status},
        )
        with sqlite3.connect(self.db_path) as con:
            con.execute(
                """
                INSERT INTO gateway_audit_events
                (id, actor, org_id, workspace_id, action, target, status, payload_json, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (event.id, event.actor, event.org_id, event.workspace_id, event.action, event.target, event.status, json.dumps(event.payload, sort_keys=True), event.created_at),
            )
        return event

    def list_events(self, limit: int = 100) -> list[dict]:
        with sqlite3.connect(self.db_path) as con:
            rows = con.execute(
                """
                SELECT id, actor, org_id, workspace_id, action, target, status, payload_json, created_at
                FROM gateway_audit_events
                ORDER BY created_at DESC LIMIT ?
                """,
                (limit,),
            ).fetchall()
        return [
            {"id": r[0], "actor": r[1], "org_id": r[2], "workspace_id": r[3], "action": r[4], "target": r[5], "status": r[6], "payload": json.loads(r[7]), "created_at": r[8]}
            for r in rows
        ]
