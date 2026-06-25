from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
import json
import uuid

from .messages import Message


@dataclass
class ChatSession:
    id: str = field(default_factory=lambda: uuid.uuid4().hex[:12])
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")
    messages: list[Message] = field(default_factory=list)

    def add(self, role: str, content: str) -> None:
        self.messages.append(Message(role=role, content=content))  # type: ignore[arg-type]

    def save(self, path: str | Path) -> Path:
        p = Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        data = {
            "id": self.id,
            "created_at": self.created_at,
            "messages": [m.to_dict() for m in self.messages],
        }
        p.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
        return p
