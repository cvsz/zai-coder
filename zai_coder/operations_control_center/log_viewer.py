"""Safe log viewer."""

from __future__ import annotations

from html import escape
from pathlib import Path

BLOCKED_PARTS = {".git", "node_modules", "apps", "release", "backups", "storage"}
ALLOWED_PREFIXES = ("logs/", "data/",)


def is_safe_log_path(path: str) -> bool:
    p = Path(path)
    normalized = str(path).replace("\\", "/")
    if p.is_absolute() or ".." in p.parts:
        return False
    if not normalized.startswith(ALLOWED_PREFIXES):
        return False
    if any(part in BLOCKED_PARTS for part in p.parts):
        return False
    return True


def tail_log(path: str = "logs/zai-coder.log", lines: int = 100) -> dict:
    if lines <= 0 or lines > 1000:
        raise ValueError("lines must be between 1 and 1000")
    if not is_safe_log_path(path):
        raise ValueError(f"unsafe log path: {path}")
    p = Path(path)
    if not p.exists():
        return {"path": path, "exists": False, "lines": []}
    raw = p.read_text(encoding="utf-8", errors="ignore")
    if "\\n" in raw and "\n" not in raw:
        raw = raw.replace("\\n", "\n")
    text_lines = raw.splitlines()
    return {"path": path, "exists": True, "lines": text_lines[-lines:]}


def render_log_viewer(result: dict) -> str:
    body = "\n".join(escape(line) for line in result.get("lines", []))
    return f"""<!doctype html><html><head><meta charset="utf-8"><title>Log Viewer</title></head><body>
<h1>Log Viewer</h1>
<p>Path: {escape(str(result.get("path", "")))}</p>
<pre>{body}</pre>
</body></html>
"""
