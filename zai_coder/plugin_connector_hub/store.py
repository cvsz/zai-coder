"""Connector installation store and audit log."""

from __future__ import annotations

import json
import sqlite3
import uuid
from pathlib import Path

from .models import ConnectorInstallation, ConnectorAuditEvent


SCHEMA = """
CREATE TABLE IF NOT EXISTS connector_installations (
    id TEXT PRIMARY KEY,
    connector_id TEXT NOT NULL,
    org_id TEXT NOT NULL,
    workspace_id TEXT NOT NULL,
    enabled INTEGER NOT NULL,
    installed_by TEXT NOT NULL,
    installed_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS connector_audit_events (
    id TEXT PRIMARY KEY,
    org_id TEXT NOT NULL,
    workspace_id TEXT NOT NULL,
    actor TEXT NOT NULL,
    action TEXT NOT NULL,
    target TEXT NOT NULL,
    payload_json TEXT NOT NULL,
    created_at TEXT NOT NULL
);
"""


class ConnectorStore:
    def __init__(self, db_path: str | Path = "data/plugin-connector-hub.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(self.db_path) as con:
            con.executescript(SCHEMA)

    def install_connector(self, connector_id: str, org_id: str, workspace_id: str, installed_by: str = "system", enabled: bool = False) -> ConnectorInstallation:
        installation = ConnectorInstallation(f"cinst_{uuid.uuid4().hex[:12]}", connector_id, org_id, workspace_id, enabled, installed_by)
        issues = installation.validate()
        if issues:
            raise ValueError("; ".join(issues))
        with sqlite3.connect(self.db_path) as con:
            con.execute(
                """
                INSERT INTO connector_installations
                (id, connector_id, org_id, workspace_id, enabled, installed_by, installed_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (installation.id, installation.connector_id, installation.org_id, installation.workspace_id, int(installation.enabled), installation.installed_by, installation.installed_at),
            )
        return installation

    def set_enabled(self, installation_id: str, enabled: bool) -> None:
        with sqlite3.connect(self.db_path) as con:
            con.execute("UPDATE connector_installations SET enabled=? WHERE id=?", (int(enabled), installation_id))

    def list_installations(self, org_id: str, workspace_id: str | None = None) -> list[dict]:
        with sqlite3.connect(self.db_path) as con:
            if workspace_id:
                rows = con.execute(
                    """
                    SELECT id, connector_id, org_id, workspace_id, enabled, installed_by, installed_at
                    FROM connector_installations WHERE org_id=? AND workspace_id=? ORDER BY installed_at DESC
                    """,
                    (org_id, workspace_id),
                ).fetchall()
            else:
                rows = con.execute(
                    """
                    SELECT id, connector_id, org_id, workspace_id, enabled, installed_by, installed_at
                    FROM connector_installations WHERE org_id=? ORDER BY installed_at DESC
                    """,
                    (org_id,),
                ).fetchall()
        return [
            {"id": r[0], "connector_id": r[1], "org_id": r[2], "workspace_id": r[3], "enabled": bool(r[4]), "installed_by": r[5], "installed_at": r[6]}
            for r in rows
        ]

    def audit(self, org_id: str, workspace_id: str, actor: str, action: str, target: str, payload: dict | None = None) -> ConnectorAuditEvent:
        event = ConnectorAuditEvent(f"cae_{uuid.uuid4().hex[:12]}", org_id, workspace_id, actor, action, target, payload or {})
        with sqlite3.connect(self.db_path) as con:
            con.execute(
                """
                INSERT INTO connector_audit_events
                (id, org_id, workspace_id, actor, action, target, payload_json, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (event.id, event.org_id, event.workspace_id, event.actor, event.action, event.target, json.dumps(event.payload, sort_keys=True), event.created_at),
            )
        return event

    def list_audit(self, org_id: str, limit: int = 100) -> list[dict]:
        with sqlite3.connect(self.db_path) as con:
            rows = con.execute(
                """
                SELECT id, org_id, workspace_id, actor, action, target, payload_json, created_at
                FROM connector_audit_events WHERE org_id=? ORDER BY created_at DESC LIMIT ?
                """,
                (org_id, limit),
            ).fetchall()
        return [
            {"id": r[0], "org_id": r[1], "workspace_id": r[2], "actor": r[3], "action": r[4], "target": r[5], "payload": json.loads(r[6]), "created_at": r[7]}
            for r in rows
        ]
