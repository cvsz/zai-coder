"""SQLite store for tenant/org/workspace runtime isolation."""

from __future__ import annotations

import json
import sqlite3
import uuid
from pathlib import Path

from .models import TenantOrg, Workspace, TenantPrincipal, TenantAuditEvent, WorkspaceQuota


SCHEMA = """
CREATE TABLE IF NOT EXISTS tenant_orgs (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    slug TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL,
    created_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS tenant_workspaces (
    id TEXT PRIMARY KEY,
    org_id TEXT NOT NULL,
    name TEXT NOT NULL,
    slug TEXT NOT NULL,
    status TEXT NOT NULL,
    created_at TEXT NOT NULL,
    UNIQUE(org_id, slug)
);
CREATE TABLE IF NOT EXISTS tenant_memberships (
    actor TEXT NOT NULL,
    org_id TEXT NOT NULL,
    workspace_id TEXT NOT NULL,
    roles_json TEXT NOT NULL,
    created_at TEXT NOT NULL,
    PRIMARY KEY(actor, org_id, workspace_id)
);
CREATE TABLE IF NOT EXISTS tenant_audit_events (
    id TEXT PRIMARY KEY,
    org_id TEXT NOT NULL,
    workspace_id TEXT NOT NULL,
    actor TEXT NOT NULL,
    action TEXT NOT NULL,
    target TEXT NOT NULL,
    payload_json TEXT NOT NULL,
    created_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS workspace_quotas (
    org_id TEXT NOT NULL,
    workspace_id TEXT NOT NULL,
    monthly_runs_limit INTEGER NOT NULL,
    storage_mb_limit INTEGER NOT NULL,
    provider_apply_limit INTEGER NOT NULL,
    PRIMARY KEY(org_id, workspace_id)
);
"""


class TenantStore:
    def __init__(self, db_path: str | Path = "data/tenant-control.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(self.db_path) as con:
            con.executescript(SCHEMA)

    def create_org(self, name: str, slug: str) -> TenantOrg:
        org = TenantOrg(id=f"org_{uuid.uuid4().hex[:12]}", name=name, slug=slug)
        issues = org.validate()
        if issues:
            raise ValueError("; ".join(issues))
        with sqlite3.connect(self.db_path) as con:
            con.execute(
                "INSERT INTO tenant_orgs (id, name, slug, status, created_at) VALUES (?, ?, ?, ?, ?)",
                (org.id, org.name, org.slug, org.status, org.created_at),
            )
        return org

    def create_workspace(self, org_id: str, name: str, slug: str) -> Workspace:
        workspace = Workspace(id=f"ws_{uuid.uuid4().hex[:12]}", org_id=org_id, name=name, slug=slug)
        issues = workspace.validate()
        if issues:
            raise ValueError("; ".join(issues))
        with sqlite3.connect(self.db_path) as con:
            con.execute(
                "INSERT INTO tenant_workspaces (id, org_id, name, slug, status, created_at) VALUES (?, ?, ?, ?, ?, ?)",
                (workspace.id, workspace.org_id, workspace.name, workspace.slug, workspace.status, workspace.created_at),
            )
        self.set_quota(WorkspaceQuota(org_id=org_id, workspace_id=workspace.id))
        return workspace

    def add_membership(self, principal: TenantPrincipal) -> TenantPrincipal:
        with sqlite3.connect(self.db_path) as con:
            con.execute(
                "INSERT OR REPLACE INTO tenant_memberships (actor, org_id, workspace_id, roles_json, created_at) VALUES (?, ?, ?, ?, ?)",
                (principal.actor, principal.org_id, principal.workspace_id, json.dumps(list(principal.roles)), principal.created_at),
            )
        return principal

    def get_membership(self, actor: str, org_id: str, workspace_id: str) -> TenantPrincipal | None:
        with sqlite3.connect(self.db_path) as con:
            row = con.execute(
                "SELECT actor, org_id, workspace_id, roles_json, created_at FROM tenant_memberships WHERE actor=? AND org_id=? AND workspace_id=?",
                (actor, org_id, workspace_id),
            ).fetchone()
        if not row:
            return None
        return TenantPrincipal(actor=row[0], org_id=row[1], workspace_id=row[2], roles=tuple(json.loads(row[3])), created_at=row[4])

    def record_audit(self, event: TenantAuditEvent) -> TenantAuditEvent:
        with sqlite3.connect(self.db_path) as con:
            con.execute(
                """
                INSERT INTO tenant_audit_events (id, org_id, workspace_id, actor, action, target, payload_json, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (event.id, event.org_id, event.workspace_id, event.actor, event.action, event.target, json.dumps(event.payload, sort_keys=True), event.created_at),
            )
        return event

    def list_audit(self, org_id: str, workspace_id: str | None = None, limit: int = 50) -> list[dict]:
        with sqlite3.connect(self.db_path) as con:
            if workspace_id:
                rows = con.execute(
                    """
                    SELECT id, org_id, workspace_id, actor, action, target, payload_json, created_at
                    FROM tenant_audit_events
                    WHERE org_id=? AND workspace_id=?
                    ORDER BY created_at DESC LIMIT ?
                    """,
                    (org_id, workspace_id, limit),
                ).fetchall()
            else:
                rows = con.execute(
                    """
                    SELECT id, org_id, workspace_id, actor, action, target, payload_json, created_at
                    FROM tenant_audit_events
                    WHERE org_id=?
                    ORDER BY created_at DESC LIMIT ?
                    """,
                    (org_id, limit),
                ).fetchall()
        return [
            {"id": r[0], "org_id": r[1], "workspace_id": r[2], "actor": r[3], "action": r[4], "target": r[5], "payload": json.loads(r[6]), "created_at": r[7]}
            for r in rows
        ]

    def set_quota(self, quota: WorkspaceQuota) -> WorkspaceQuota:
        issues = quota.validate()
        if issues:
            raise ValueError("; ".join(issues))
        with sqlite3.connect(self.db_path) as con:
            con.execute(
                """
                INSERT OR REPLACE INTO workspace_quotas
                (org_id, workspace_id, monthly_runs_limit, storage_mb_limit, provider_apply_limit)
                VALUES (?, ?, ?, ?, ?)
                """,
                (quota.org_id, quota.workspace_id, quota.monthly_runs_limit, quota.storage_mb_limit, quota.provider_apply_limit),
            )
        return quota

    def get_quota(self, org_id: str, workspace_id: str) -> WorkspaceQuota | None:
        with sqlite3.connect(self.db_path) as con:
            row = con.execute(
                """
                SELECT org_id, workspace_id, monthly_runs_limit, storage_mb_limit, provider_apply_limit
                FROM workspace_quotas WHERE org_id=? AND workspace_id=?
                """,
                (org_id, workspace_id),
            ).fetchone()
        if not row:
            return None
        return WorkspaceQuota(org_id=row[0], workspace_id=row[1], monthly_runs_limit=row[2], storage_mb_limit=row[3], provider_apply_limit=row[4])
