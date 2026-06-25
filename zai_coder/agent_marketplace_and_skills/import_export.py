"""Offline marketplace import/export."""

from __future__ import annotations

import json
from pathlib import Path

from .catalog import skill_catalog, agent_catalog


def export_marketplace_bundle(root: str | Path = ".", out: str = "marketplace/exports/marketplace-bundle.json") -> str:
    root = Path(root)
    path = root / out
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {"skills": skill_catalog(), "agents": agent_catalog(), "offline": True}
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    return str(path)


def validate_import_bundle(payload: dict) -> dict:
    issues = []
    if "skills" not in payload or "agents" not in payload:
        issues.append("bundle must contain skills and agents")
    if payload.get("offline") is not True:
        issues.append("bundle must be offline=true")
    return {"ok": not issues, "issues": issues, "counts": {"skills": len(payload.get("skills", [])), "agents": len(payload.get("agents", []))}}
