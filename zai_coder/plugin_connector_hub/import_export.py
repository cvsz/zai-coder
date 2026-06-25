"""Offline connector manifest import/export."""

from __future__ import annotations

import json
from pathlib import Path

from .catalog import connector_catalog


def export_connector_bundle(root: str | Path = ".", out: str = "connectors/exports/connector-bundle.json") -> str:
    root = Path(root)
    path = root / out
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {"kind": "zai-connector-bundle", "version": "1.0", "offline": True, "connectors": connector_catalog()}
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    return str(path)


def validate_connector_bundle(payload: dict) -> dict:
    issues = []
    if payload.get("kind") != "zai-connector-bundle":
        issues.append("kind must be zai-connector-bundle")
    if payload.get("offline") is not True:
        issues.append("offline must be true")
    if "connectors" not in payload:
        issues.append("connectors required")
    return {"ok": not issues, "issues": issues, "count": len(payload.get("connectors", []))}
