"""Alembic-style migration manager.

This keeps a deterministic revision table and supports dry-run planning.
"""

from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


BOOTSTRAP = """
CREATE TABLE IF NOT EXISTS production_schema_revisions (
    revision TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    applied_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
"""


@dataclass(frozen=True)
class Revision:
    revision: str
    name: str
    sql: str
    down_sql: str = ""

    def to_dict(self) -> dict:
        return {"revision": self.revision, "name": self.name, "sql": self.sql, "down_sql": self.down_sql}


DEFAULT_REVISIONS = [
    Revision(
        "20260625_0001",
        "production_sessions",
        """
        CREATE TABLE IF NOT EXISTS production_audit_log (
            id TEXT PRIMARY KEY,
            actor TEXT NOT NULL,
            action TEXT NOT NULL,
            target TEXT NOT NULL,
            payload_json TEXT NOT NULL,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
        """,
    ),
    Revision(
        "20260625_0002",
        "production_jobs",
        """
        CREATE TABLE IF NOT EXISTS production_jobs (
            id TEXT PRIMARY KEY,
            job_type TEXT NOT NULL,
            payload_json TEXT NOT NULL,
            status TEXT NOT NULL,
            attempts INTEGER NOT NULL DEFAULT 0,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
        """,
    ),
]


class RevisionManager:
    def __init__(self, db_path: str | Path, revisions: Iterable[Revision] | None = None):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.revisions = list(revisions or DEFAULT_REVISIONS)

    def applied_revisions(self) -> set[str]:
        with sqlite3.connect(self.db_path) as con:
            con.executescript(BOOTSTRAP)
            return {row[0] for row in con.execute("SELECT revision FROM production_schema_revisions").fetchall()}

    def plan(self) -> list[Revision]:
        applied = self.applied_revisions()
        return [revision for revision in self.revisions if revision.revision not in applied]

    def upgrade(self, apply: bool = False) -> list[dict]:
        pending = self.plan()
        if not apply:
            return [{"dry_run": True, **revision.to_dict()} for revision in pending]
        applied = []
        with sqlite3.connect(self.db_path) as con:
            con.executescript(BOOTSTRAP)
            for revision in pending:
                con.executescript(revision.sql)
                con.execute(
                    "INSERT INTO production_schema_revisions (revision, name) VALUES (?, ?)",
                    (revision.revision, revision.name),
                )
                applied.append({"dry_run": False, **revision.to_dict()})
        return applied
