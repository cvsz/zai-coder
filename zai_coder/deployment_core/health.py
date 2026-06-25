"""Deployment health checks."""

from __future__ import annotations

import os
import shutil
import sqlite3
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class HealthResult:
    name: str
    ok: bool
    detail: str

    def to_dict(self) -> dict:
        return {"name": self.name, "ok": self.ok, "detail": self.detail}


def check_sqlite(db_path: str | Path) -> HealthResult:
    try:
        path = Path(db_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(path) as con:
            con.execute("SELECT 1")
        return HealthResult("sqlite", True, str(path))
    except Exception as exc:
        return HealthResult("sqlite", False, str(exc))


def run_deployment_health(project_root: str | Path = ".", db_path: str | Path = "data/zai-app.db") -> list[HealthResult]:
    root = Path(project_root)
    return [
        HealthResult("python", sys.version_info >= (3, 10), sys.version.split()[0]),
        HealthResult("project_root", root.exists(), str(root.resolve())),
        HealthResult("git", shutil.which("git") is not None, shutil.which("git") or "not found"),
        HealthResult("docker", shutil.which("docker") is not None, shutil.which("docker") or "not found"),
        HealthResult("gh", shutil.which("gh") is not None, shutil.which("gh") or "not found"),
        check_sqlite(db_path),
    ]


def health_summary(results: list[HealthResult]) -> dict:
    return {
        "ok": all(r.ok for r in results),
        "checks": [r.to_dict() for r in results],
    }
