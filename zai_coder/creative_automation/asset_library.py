"""Unified creative asset library.

All paths are local, relative, and safety-checked. No external upload happens here.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable, List


ALLOWED_EXTENSIONS = {
    ".md", ".txt", ".html", ".json", ".csv",
    ".png", ".jpg", ".jpeg", ".webp", ".svg",
    ".wav", ".mp3", ".ogg",
    ".glb", ".gltf", ".tmx", ".tsx",
    ".srt", ".vtt",
}


@dataclass
class CreativeAsset:
    path: str
    kind: str
    project_slug: str = ""
    tags: List[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "path": self.path,
            "kind": self.kind,
            "project_slug": self.project_slug,
            "tags": list(self.tags),
        }


def is_safe_asset_path(path: str) -> bool:
    p = Path(path)
    normalized = str(path).replace("\\", "/")
    if p.is_absolute() or ".." in p.parts:
        return False
    if normalized.startswith("apps/zlms/"):
        return False
    if any(part in p.parts for part in {"node_modules", "dist", ".next", "coverage", "reports", "__pycache__", ".pytest_cache"}):
        return False
    if p.name.startswith(".env"):
        return False
    return p.suffix.lower() in ALLOWED_EXTENSIONS


def build_asset_library(paths: Iterable[str], project_slug: str = "") -> List[CreativeAsset]:
    assets: list[CreativeAsset] = []
    for path in paths:
        if not is_safe_asset_path(path):
            continue
        suffix = Path(path).suffix.lower().lstrip(".")
        assets.append(CreativeAsset(path=path, kind=suffix, project_slug=project_slug))
    return assets
