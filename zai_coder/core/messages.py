from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Literal

Role = Literal["system", "user", "assistant", "tool"]


@dataclass
class Message:
    role: Role
    content: str

    def to_dict(self) -> dict[str, str]:
        return asdict(self)
