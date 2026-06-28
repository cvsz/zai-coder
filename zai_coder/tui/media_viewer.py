from __future__ import annotations

import os
import mimetypes
import base64
from pathlib import Path


def is_supported_image(path: str | Path) -> bool:
    mime, _ = mimetypes.guess_type(str(path))
    if mime and mime.startswith("image/"):
        return mime in {"image/jpeg", "image/png", "image/webp", "image/gif"}
    return False

def render_kitty_protocol(path: Path) -> str:
    try:
        with open(path, "rb") as f:
            data = f.read()
        b64_data = base64.standard_b64encode(data).decode('ascii')
        return f"\033_Ga=T,f=100;{b64_data}\033\\"
    except Exception as e:
        return f"[MEDIA VIEWER]\nError rendering image: {e}"

def render_sixel_protocol(path: Path) -> str:
    # Just returning a placeholder if real sixel conversion is not installed
    return f"[MEDIA VIEWER]\n(Sixel format display for {path.name})"

def render_media_viewer(file_path: str | Path | None) -> str:
    if not file_path:
        return "[MEDIA VIEWER]\nNo media selected."
    
    path = Path(file_path)
    if not path.exists():
        return f"[MEDIA VIEWER]\nFile not found: {file_path}"
    
    if is_supported_image(path):
        term = os.environ.get("TERM", "")
        # Very simple detection for kitty
        if "kitty" in term.lower() or os.environ.get("KITTY_WINDOW_ID"):
            return render_kitty_protocol(path)
        # Sixel detection could be more robust, but just fallback
        if "xterm" in term.lower():
            return render_sixel_protocol(path)
            
        return f"[MEDIA VIEWER]\nDisplaying image: {path.name}\n(Terminal rendering not supported by environment)"
    
    return f"[MEDIA VIEWER]\nUnsupported media format: {path.name}"
