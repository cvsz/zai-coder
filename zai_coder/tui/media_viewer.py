from __future__ import annotations

import mimetypes
from pathlib import Path


def is_supported_image(path: str | Path) -> bool:
    mime, _ = mimetypes.guess_type(str(path))
    if mime and mime.startswith("image/"):
        return mime in {"image/jpeg", "image/png", "image/webp", "image/gif"}
    return False


def render_media_viewer(file_path: str | Path | None) -> str:
    if not file_path:
        return "[MEDIA VIEWER]\nNo media selected."
    
    path = Path(file_path)
    if not path.exists():
        return f"[MEDIA VIEWER]\nFile not found: {file_path}"
    
    if is_supported_image(path):
        return f"[MEDIA VIEWER]\nDisplaying image: {path.name}\n(Terminal rendering abstracted)"
    
    return f"[MEDIA VIEWER]\nUnsupported media format: {path.name}"
