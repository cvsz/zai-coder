from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class AgentContext:
    task: str
    memory: dict[str, Any] = field(default_factory=dict)


class Agent:
    name = "base"
    description = "Base agent"

    def build_prompt(self, context: AgentContext) -> str:
        return context.task
