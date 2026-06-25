"""Shared marketing asset registry."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List


ALLOWED_ASSET_EXTENSIONS = {".md", ".txt", ".png", ".jpg", ".jpeg", ".svg", ".webp", ".json"}


@dataclass
class MarketingAsset:
    path: str
    kind: str
    tags: list[str]

    def to_dict(self) -> dict:
        return {"path": self.path, "kind": self.kind, "tags": list(self.tags)}


def is_allowed_asset(path: str) -> bool:
    p = Path(path)
    if p.is_absolute() or ".." in p.parts:
        return False
    if str(path).replace("\\", "/").startswith("apps/zlms/"):
        return False
    return p.suffix.lower() in ALLOWED_ASSET_EXTENSIONS


def build_asset_manifest(paths: Iterable[str]) -> List[MarketingAsset]:
    assets: list[MarketingAsset] = []
    for path in paths:
        if not is_allowed_asset(path):
            continue
        suffix = Path(path).suffix.lower().lstrip(".")
        assets.append(MarketingAsset(path=path, kind=suffix, tags=[]))
    return assets
