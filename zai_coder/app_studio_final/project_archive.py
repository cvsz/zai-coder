"""Project export/import archive helpers."""

from __future__ import annotations

import json
import zipfile
from pathlib import Path


BLOCKED_PARTS = {".git", "node_modules", "dist", ".next", "coverage", "reports", "__pycache__", ".pytest_cache"}


def is_archive_safe(rel: Path) -> bool:
    normalized = str(rel).replace("\\", "/")
    if rel.is_absolute() or ".." in rel.parts:
        return False
    if normalized.startswith("apps/zlms/"):
        return False
    if any(part in BLOCKED_PARTS for part in rel.parts):
        return False
    if rel.name.startswith(".env"):
        return False
    return True


def export_project_archive(project_root: str | Path, archive_path: str | Path, manifest: dict | None = None, apply: bool = False) -> dict:
    root = Path(project_root)
    archive = Path(archive_path)
    files = [p for p in root.rglob("*") if p.is_file() and is_archive_safe(p.relative_to(root))]
    if not apply:
        return {"dry_run": True, "archive": str(archive), "file_count": len(files)}
    archive.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED) as z:
        z.writestr("zai-project-manifest.json", json.dumps(manifest or {}, indent=2))
        for p in files:
            z.write(p, p.relative_to(root))
    return {"dry_run": False, "archive": str(archive), "file_count": len(files)}


def inspect_project_archive(archive_path: str | Path) -> dict:
    archive = Path(archive_path)
    with zipfile.ZipFile(archive) as z:
        names = z.namelist()
    unsafe = [name for name in names if not is_archive_safe(Path(name)) and name != "zai-project-manifest.json"]
    return {"archive": str(archive), "file_count": len(names), "unsafe": unsafe}
