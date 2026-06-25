from __future__ import annotations

import json
import re
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

SECRET_PATTERNS = [
    re.compile(r"sk-[A-Za-z0-9_\-]{20,}"),
    re.compile(r"sk-or-v1-[A-Za-z0-9_\-]{20,}"),
    re.compile(r"ghp_[A-Za-z0-9_]{20,}"),
    re.compile(r"AIza[A-Za-z0-9_\-]{20,}"),
]


def redact(value: str) -> str:
    out = value
    for pattern in SECRET_PATTERNS:
        out = pattern.sub("[REDACTED_SECRET]", out)
    return out


@dataclass
class AuditEvent:
    ts: float
    action: str
    ok: bool
    summary: str
    details: dict[str, Any]


class AuditLog:
    def __init__(self, path: str | Path):
        self.path = Path(path).expanduser()
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def write(self, action: str, ok: bool, summary: str, **details: Any) -> None:
        clean_details = json.loads(redact(json.dumps(details, ensure_ascii=False, default=str)))
        event = AuditEvent(time.time(), action, ok, redact(summary), clean_details)
        with self.path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(asdict(event), ensure_ascii=False) + "\n")

    def tail(self, limit: int = 50) -> list[dict[str, Any]]:
        if not self.path.exists():
            return []
        lines = self.path.read_text(encoding="utf-8", errors="replace").splitlines()[-limit:]
        result = []
        for line in lines:
            try:
                result.append(json.loads(line))
            except json.JSONDecodeError:
                continue
        return result
