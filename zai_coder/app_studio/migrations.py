"""SQLite migration manager for local App Studio deployments."""

from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List


BOOTSTRAP = """
CREATE TABLE IF NOT EXISTS schema_migrations (
    version TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    applied_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
"""


@dataclass(frozen=True)
class Migration:
    version: str
    name: str
    sql: str

    def to_dict(self) -> dict:
        return {"version": self.version, "name": self.name, "sql": self.sql}


DEFAULT_MIGRATIONS = [
    Migration(
        version="001",
        name="app_studio_core",
        sql="""
        CREATE TABLE IF NOT EXISTS app_studio_projects (
            id TEXT PRIMARY KEY,
            slug TEXT NOT NULL UNIQUE,
            title TEXT NOT NULL,
            project_type TEXT NOT NULL,
            status TEXT NOT NULL,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
        """,
    ),
    Migration(
        version="002",
        name="app_studio_runs",
        sql="""
        CREATE TABLE IF NOT EXISTS app_studio_runs (
            id TEXT PRIMARY KEY,
            project_slug TEXT NOT NULL,
            run_type TEXT NOT NULL,
            status TEXT NOT NULL,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
        """,
    ),
    Migration(
        version="003",
        name="app_studio_audit",
        sql="""
        CREATE TABLE IF NOT EXISTS app_studio_audit (
            id TEXT PRIMARY KEY,
            actor TEXT NOT NULL,
            action TEXT NOT NULL,
            target TEXT NOT NULL,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
        """,
    ),
]


class MigrationManager:
    def __init__(self, db_path: str | Path, migrations: Iterable[Migration] | None = None):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.migrations = list(migrations or DEFAULT_MIGRATIONS)

    def plan(self) -> list[Migration]:
        with sqlite3.connect(self.db_path) as con:
            con.executescript(BOOTSTRAP)
            applied = {row[0] for row in con.execute("SELECT version FROM schema_migrations").fetchall()}
        return [m for m in self.migrations if m.version not in applied]

    def apply(self, apply: bool = False) -> list[dict]:
        pending = self.plan()
        if not apply:
            return [{"dry_run": True, **m.to_dict()} for m in pending]
        applied: List[dict] = []
        with sqlite3.connect(self.db_path) as con:
            con.executescript(BOOTSTRAP)
            for m in pending:
                con.executescript(m.sql)
                con.execute(
                    "INSERT INTO schema_migrations (version, name) VALUES (?, ?)",
                    (m.version, m.name),
                )
                applied.append({"dry_run": False, **m.to_dict()})
        return applied
