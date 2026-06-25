"""Skill installation store and marketplace audit."""

from __future__ import annotations

import json
import sqlite3
import uuid
from pathlib import Path

from .models import SkillInstallation, MarketplaceAuditEvent, SkillReview


SCHEMA = """
CREATE TABLE IF NOT EXISTS skill_installations (
    id TEXT PRIMARY KEY,
    skill_id TEXT NOT NULL,
    org_id TEXT NOT NULL,
    workspace_id TEXT NOT NULL,
    enabled INTEGER NOT NULL,
    installed_by TEXT NOT NULL,
    installed_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS marketplace_audit_events (
    id TEXT PRIMARY KEY,
    org_id TEXT NOT NULL,
    workspace_id TEXT NOT NULL,
    actor TEXT NOT NULL,
    action TEXT NOT NULL,
    target TEXT NOT NULL,
    payload_json TEXT NOT NULL,
    created_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS skill_reviews (
    id TEXT PRIMARY KEY,
    skill_id TEXT NOT NULL,
    reviewer TEXT NOT NULL,
    rating INTEGER NOT NULL,
    comment TEXT NOT NULL,
    created_at TEXT NOT NULL
);
"""


class MarketplaceStore:
    def __init__(self, db_path: str | Path = "data/agent-marketplace.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(self.db_path) as con:
            con.executescript(SCHEMA)

    def install_skill(self, skill_id: str, org_id: str, workspace_id: str, installed_by: str = "system", enabled: bool = False) -> SkillInstallation:
        installation = SkillInstallation(f"inst_{uuid.uuid4().hex[:12]}", skill_id, org_id, workspace_id, enabled, installed_by)
        issues = installation.validate()
        if issues:
            raise ValueError("; ".join(issues))
        with sqlite3.connect(self.db_path) as con:
            con.execute(
                """
                INSERT INTO skill_installations
                (id, skill_id, org_id, workspace_id, enabled, installed_by, installed_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (installation.id, installation.skill_id, installation.org_id, installation.workspace_id, int(installation.enabled), installation.installed_by, installation.installed_at),
            )
        return installation

    def set_enabled(self, installation_id: str, enabled: bool) -> None:
        with sqlite3.connect(self.db_path) as con:
            con.execute("UPDATE skill_installations SET enabled=? WHERE id=?", (int(enabled), installation_id))

    def list_installations(self, org_id: str, workspace_id: str | None = None) -> list[dict]:
        with sqlite3.connect(self.db_path) as con:
            if workspace_id:
                rows = con.execute(
                    """
                    SELECT id, skill_id, org_id, workspace_id, enabled, installed_by, installed_at
                    FROM skill_installations WHERE org_id=? AND workspace_id=? ORDER BY installed_at DESC
                    """,
                    (org_id, workspace_id),
                ).fetchall()
            else:
                rows = con.execute(
                    """
                    SELECT id, skill_id, org_id, workspace_id, enabled, installed_by, installed_at
                    FROM skill_installations WHERE org_id=? ORDER BY installed_at DESC
                    """,
                    (org_id,),
                ).fetchall()
        return [
            {"id": r[0], "skill_id": r[1], "org_id": r[2], "workspace_id": r[3], "enabled": bool(r[4]), "installed_by": r[5], "installed_at": r[6]}
            for r in rows
        ]

    def audit(self, org_id: str, workspace_id: str, actor: str, action: str, target: str, payload: dict | None = None) -> MarketplaceAuditEvent:
        event = MarketplaceAuditEvent(f"mae_{uuid.uuid4().hex[:12]}", org_id, workspace_id, actor, action, target, payload or {})
        with sqlite3.connect(self.db_path) as con:
            con.execute(
                """
                INSERT INTO marketplace_audit_events
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
                FROM marketplace_audit_events WHERE org_id=? ORDER BY created_at DESC LIMIT ?
                """,
                (org_id, limit),
            ).fetchall()
        return [
            {"id": r[0], "org_id": r[1], "workspace_id": r[2], "actor": r[3], "action": r[4], "target": r[5], "payload": json.loads(r[6]), "created_at": r[7]}
            for r in rows
        ]

    def add_review(self, skill_id: str, reviewer: str, rating: int, comment: str) -> SkillReview:
        review = SkillReview(f"rev_{uuid.uuid4().hex[:12]}", skill_id, reviewer, rating, comment)
        issues = review.validate()
        if issues:
            raise ValueError("; ".join(issues))
        with sqlite3.connect(self.db_path) as con:
            con.execute(
                "INSERT INTO skill_reviews (id, skill_id, reviewer, rating, comment, created_at) VALUES (?, ?, ?, ?, ?, ?)",
                (review.id, review.skill_id, review.reviewer, review.rating, review.comment, review.created_at),
            )
        return review

    def list_reviews(self, skill_id: str) -> list[dict]:
        with sqlite3.connect(self.db_path) as con:
            rows = con.execute(
                "SELECT id, skill_id, reviewer, rating, comment, created_at FROM skill_reviews WHERE skill_id=? ORDER BY created_at DESC",
                (skill_id,),
            ).fetchall()
        return [SkillReview(r[0], r[1], r[2], r[3], r[4], r[5]).to_dict() for r in rows]
