"""SQLite store for production SaaS core."""

from __future__ import annotations

import sqlite3
import uuid
from pathlib import Path
from typing import List

from .models import Organization, Workspace, UserAccount, Invitation


SCHEMA = """
CREATE TABLE IF NOT EXISTS saas_users (
    id TEXT PRIMARY KEY,
    email TEXT NOT NULL UNIQUE,
    display_name TEXT NOT NULL,
    status TEXT NOT NULL,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS saas_organizations (
    id TEXT PRIMARY KEY,
    slug TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    owner_user_id TEXT NOT NULL,
    plan_slug TEXT NOT NULL,
    status TEXT NOT NULL,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS saas_workspaces (
    id TEXT PRIMARY KEY,
    org_id TEXT NOT NULL,
    slug TEXT NOT NULL,
    name TEXT NOT NULL,
    status TEXT NOT NULL,
    created_at TEXT NOT NULL,
    UNIQUE(org_id, slug)
);

CREATE TABLE IF NOT EXISTS saas_invitations (
    id TEXT PRIMARY KEY,
    org_id TEXT NOT NULL,
    email TEXT NOT NULL,
    role TEXT NOT NULL,
    invited_by_user_id TEXT NOT NULL,
    status TEXT NOT NULL,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS saas_memberships (
    org_id TEXT NOT NULL,
    user_id TEXT NOT NULL,
    role TEXT NOT NULL,
    status TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY(org_id, user_id)
);
"""


class SaasStore:
    def __init__(self, db_path: str | Path):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(self.db_path) as con:
            con.executescript(SCHEMA)

    def create_user(self, email: str, display_name: str) -> UserAccount:
        user = UserAccount(id=str(uuid.uuid4()), email=email.strip().lower(), display_name=display_name.strip())
        issues = user.validate()
        if issues:
            raise ValueError("; ".join(issues))
        with sqlite3.connect(self.db_path) as con:
            con.execute(
                "INSERT INTO saas_users (id, email, display_name, status, created_at) VALUES (?, ?, ?, ?, ?)",
                (user.id, user.email, user.display_name, user.status, user.created_at),
            )
        return user

    def create_organization(self, slug: str, name: str, owner_user_id: str, plan_slug: str = "free") -> Organization:
        org = Organization(id=str(uuid.uuid4()), slug=slug, name=name, owner_user_id=owner_user_id, plan_slug=plan_slug)
        issues = org.validate()
        if issues:
            raise ValueError("; ".join(issues))
        with sqlite3.connect(self.db_path) as con:
            con.execute(
                """
                INSERT INTO saas_organizations
                (id, slug, name, owner_user_id, plan_slug, status, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (org.id, org.slug, org.name, org.owner_user_id, org.plan_slug, org.status, org.created_at),
            )
            con.execute(
                "INSERT INTO saas_memberships (org_id, user_id, role, status) VALUES (?, ?, ?, ?)",
                (org.id, owner_user_id, "owner", "active"),
            )
        return org

    def create_workspace(self, org_id: str, slug: str, name: str) -> Workspace:
        workspace = Workspace(id=str(uuid.uuid4()), org_id=org_id, slug=slug, name=name)
        issues = workspace.validate()
        if issues:
            raise ValueError("; ".join(issues))
        with sqlite3.connect(self.db_path) as con:
            con.execute(
                "INSERT INTO saas_workspaces (id, org_id, slug, name, status, created_at) VALUES (?, ?, ?, ?, ?, ?)",
                (workspace.id, workspace.org_id, workspace.slug, workspace.name, workspace.status, workspace.created_at),
            )
        return workspace

    def create_invitation(self, org_id: str, email: str, role: str, invited_by_user_id: str) -> Invitation:
        invitation = Invitation(id=str(uuid.uuid4()), org_id=org_id, email=email.strip().lower(), role=role, invited_by_user_id=invited_by_user_id)
        issues = invitation.validate()
        if issues:
            raise ValueError("; ".join(issues))
        with sqlite3.connect(self.db_path) as con:
            con.execute(
                """
                INSERT INTO saas_invitations
                (id, org_id, email, role, invited_by_user_id, status, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (invitation.id, invitation.org_id, invitation.email, invitation.role, invitation.invited_by_user_id, invitation.status, invitation.created_at),
            )
        return invitation

    def list_organizations(self) -> List[Organization]:
        with sqlite3.connect(self.db_path) as con:
            rows = con.execute(
                "SELECT id, slug, name, owner_user_id, plan_slug, status, created_at FROM saas_organizations ORDER BY created_at"
            ).fetchall()
        return [Organization(*row) for row in rows]

    def count_workspaces(self, org_id: str) -> int:
        with sqlite3.connect(self.db_path) as con:
            return int(con.execute("SELECT COUNT(*) FROM saas_workspaces WHERE org_id = ?", (org_id,)).fetchone()[0])

    def count_members(self, org_id: str) -> int:
        with sqlite3.connect(self.db_path) as con:
            return int(con.execute("SELECT COUNT(*) FROM saas_memberships WHERE org_id = ? AND status = 'active'", (org_id,)).fetchone()[0])
