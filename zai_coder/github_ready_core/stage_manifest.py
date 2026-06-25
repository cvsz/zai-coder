from __future__ import annotations

from pathlib import Path
from typing import Iterable
from .repo_policy import is_safe_stage_path

def load_stage_manifest(path: str | Path) -> list[str]:
    manifest = Path(path)
    if not manifest.exists():
        raise FileNotFoundError(str(manifest))
    items = []
    for line in manifest.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped and not stripped.startswith("#"):
            items.append(stripped)
    return items

def validate_stage_manifest(paths: Iterable[str]) -> dict:
    safe, blocked = [], []
    for item in paths:
        (safe if is_safe_stage_path(item) else blocked).append(item)
    return {"ok": not blocked, "safe": safe, "blocked": blocked}

def render_git_add_commands(paths: Iterable[str]) -> list[str]:
    result = validate_stage_manifest(paths)
    if result["blocked"]:
        raise ValueError(f"blocked unsafe stage paths: {result['blocked']}")
    return [f"git add -- {path}" for path in result["safe"]]
