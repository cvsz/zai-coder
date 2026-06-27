from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Literal

Role = Literal["system", "user", "assistant", "tool"]


@dataclass
class Message:
    role: Role
    content: str | list[dict]

    def to_dict(self) -> dict:
        return {"role": self.role, "content": self.content}
