"""Health and readiness payloads."""

from __future__ import annotations

import os
import platform
import sqlite3
from pathlib import Path


def health_payload(settings: dict) -> dict:
    return {
        "ok": True,
        "service": "zai-coder-control-plane",
        "environment": settings.get("environment", "production"),
        "python": platform.python_version(),
    }


def readiness_payload(settings: dict) -> dict:
    checks = []
    session_db = Path(settings.get("session_db_path", "data/zai-sessions.db"))
    try:
        session_db.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(session_db) as con:
            con.execute("SELECT 1")
        checks.append({"name": "session-db", "ok": True})
    except Exception as exc:
        checks.append({"name": "session-db", "ok": False, "detail": str(exc)})
    checks.append({"name": "env", "ok": bool(settings.get("environment"))})
    return {"ok": all(c["ok"] for c in checks), "checks": checks}
