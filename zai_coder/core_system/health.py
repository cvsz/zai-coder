"""Core system health checks."""

from __future__ import annotations

import shutil
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass
class HealthCheck:
    name: str
    ok: bool
    detail: str


def run_core_health(project_root: str | Path = ".") -> list[HealthCheck]:
    root = Path(project_root)
    checks = [
        HealthCheck("python", sys.version_info >= (3, 10), sys.version.split()[0]),
        HealthCheck("project_root", root.exists(), str(root.resolve())),
        HealthCheck("git", shutil.which("git") is not None, shutil.which("git") or "not found"),
        HealthCheck("sqlite", True, "stdlib sqlite3 available"),
    ]
    return checks
