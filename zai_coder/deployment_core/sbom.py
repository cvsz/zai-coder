"""Minimal SBOM generator.

This produces a small JSON inventory of files and Python modules in the package.
"""

from __future__ import annotations

import json
from pathlib import Path


BLOCKED_DIRS = {".git", "__pycache__", ".pytest_cache", "node_modules", "dist", ".next", "coverage", "reports"}


def generate_minimal_sbom(root: str | Path) -> dict:
    root = Path(root)
    components = []
    for path in root.rglob("*"):
        rel = path.relative_to(root)
        if any(part in BLOCKED_DIRS for part in rel.parts):
            continue
        if path.is_file():
            components.append({
                "path": str(rel),
                "type": "python" if path.suffix == ".py" else "file",
                "size": path.stat().st_size,
            })
    return {"format": "zai-minimal-sbom-v1", "components": components}


def write_sbom(root: str | Path, out_file: str | Path = "SBOM.json") -> dict:
    sbom = generate_minimal_sbom(root)
    Path(out_file).write_text(json.dumps(sbom, indent=2) + "\n", encoding="utf-8")
    return sbom
