"""Safe game asset path handling."""

from __future__ import annotations

from pathlib import Path


ALLOWED_GAME_ASSET_EXTENSIONS = {
    ".png", ".jpg", ".jpeg", ".webp", ".svg",
    ".wav", ".mp3", ".ogg",
    ".json", ".tmx", ".tsx", ".glb", ".gltf",
}


def is_safe_game_asset_path(path: str) -> bool:
    p = Path(path)
    normalized = str(path).replace("\\", "/")
    if p.is_absolute() or ".." in p.parts:
        return False
    if normalized.startswith("apps/zlms/"):
        return False
    if any(part in p.parts for part in {"node_modules", "dist", ".next", "coverage", "reports"}):
        return False
    return p.suffix.lower() in ALLOWED_GAME_ASSET_EXTENSIONS
