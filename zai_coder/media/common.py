from __future__ import annotations

import re
from pathlib import Path


def ensure_out(path: str) -> Path:
    p = Path(path).expanduser()
    p.parent.mkdir(parents=True, exist_ok=True)
    return p


def safe_text(text: str, limit: int = 120) -> str:
    text = re.sub(r"\s+", " ", text.strip())
    return text[:limit]
