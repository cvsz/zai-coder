"""Feedback and roadmap export helpers."""

from __future__ import annotations

import json
from pathlib import Path

from .roadmap import roadmap_by_visibility, roadmap_validation_report
from .changelog_loop import changelog_feedback_prompt


def roadmap_export_bundle(visibility: str = "customer") -> dict:
    return {
        "kind": "zai-roadmap-export",
        "version": "1.0",
        "visibility": visibility,
        "roadmap": roadmap_by_visibility(visibility),
        "validation": roadmap_validation_report(),
        "changelog_feedback_prompt": changelog_feedback_prompt(),
        "external_publish": False,
        "requires_review": True,
    }


def write_roadmap_export(root: str | Path = ".", visibility: str = "customer", out: str = "roadmap/exports/roadmap-export.json") -> str:
    root = Path(root)
    path = root / out
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(roadmap_export_bundle(visibility), indent=2, sort_keys=True), encoding="utf-8")
    return str(path)
