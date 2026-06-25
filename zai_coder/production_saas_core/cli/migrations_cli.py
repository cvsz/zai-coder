"""Database migrations CLI facade."""

from __future__ import annotations

from pathlib import Path

from zai_coder.app_studio.migrations import MigrationManager


def migrations_command(db_path: str | Path = "data/zai-app.db", apply: bool = False) -> dict:
    manager = MigrationManager(db_path)
    return {"apply": apply, "migrations": manager.apply(apply=apply)}
