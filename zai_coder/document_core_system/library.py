"""Safe local document library index."""

from __future__ import annotations

from pathlib import Path


ALLOWED_DOCUMENT_EXTENSIONS = {".md", ".txt", ".html", ".json", ".csv"}


def is_safe_document_path(path: str) -> bool:
    p = Path(path)
    normalized = str(path).replace("\\", "/")
    if p.is_absolute() or ".." in p.parts:
        return False
    if normalized.startswith("apps/zlms/"):
        return False
    if any(part in p.parts for part in {"node_modules", "dist", ".next", "coverage", "reports"}):
        return False
    return p.suffix.lower() in ALLOWED_DOCUMENT_EXTENSIONS
