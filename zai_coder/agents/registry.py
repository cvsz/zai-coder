from __future__ import annotations

from .base import Agent
from .coder import CoderAgent
from .planner import PlannerAgent
from .reviewer import ReviewerAgent
from .media import MediaAgent

AGENTS: dict[str, type[Agent]] = {
    "planner": PlannerAgent,
    "coder": CoderAgent,
    "reviewer": ReviewerAgent,
    "media": MediaAgent,
}


def build_agent(name: str) -> Agent:
    cls = AGENTS.get(name)
    if not cls:
        raise KeyError(f"Unknown agent: {name}. Available: {', '.join(sorted(AGENTS))}")
    return cls()
