"""Dependency-free route registry for creative automation API.

This is framework-neutral; the existing server can map these handlers to HTTP routes.
"""

from __future__ import annotations

from .project_types import CREATIVE_PROJECT_TYPES
from .asset_library import build_asset_library
from .export_adapters import phaser_export_plan, godot_export_plan


def route_status() -> dict:
    return {
        "ok": True,
        "service": "creative-automation",
        "project_types": CREATIVE_PROJECT_TYPES,
    }


def route_assets(payload: dict) -> dict:
    paths = payload.get("paths", [])
    project_slug = payload.get("project_slug", "")
    assets = build_asset_library(paths, project_slug=project_slug)
    return {"assets": [a.to_dict() for a in assets]}


def route_export_plan(payload: dict) -> dict:
    kind = payload.get("kind")
    if kind == "phaser":
        return phaser_export_plan(payload.get("slug", "game"), payload.get("title", "Game")).to_dict()
    if kind == "godot":
        return godot_export_plan(payload.get("slug", "game"), payload.get("title", "Game")).to_dict()
    return {"error": f"unsupported export kind: {kind}"}
