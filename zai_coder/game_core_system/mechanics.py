"""Game mechanics scaffolding."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass
class Mechanic:
    name: str
    trigger: str
    rule: str
    feedback: str

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "trigger": self.trigger,
            "rule": self.rule,
            "feedback": self.feedback,
        }


def validate_mechanics(mechanics: List[Mechanic]) -> list[str]:
    issues: list[str] = []
    seen = set()
    for mechanic in mechanics:
        key = mechanic.name.strip().lower()
        if key in seen:
            issues.append(f"duplicate mechanic: {mechanic.name}")
        seen.add(key)
        if not mechanic.trigger:
            issues.append(f"missing trigger: {mechanic.name}")
        if not mechanic.rule:
            issues.append(f"missing rule: {mechanic.name}")
    return issues
