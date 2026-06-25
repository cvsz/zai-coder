"""Movie production planning helpers."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass
class ProductionTask:
    title: str
    owner: str
    status: str = "todo"

    def to_dict(self) -> dict:
        return {"title": self.title, "owner": self.owner, "status": self.status}


def validate_production_tasks(tasks: List[ProductionTask]) -> list[str]:
    issues: list[str] = []
    for task in tasks:
        if not task.title:
            issues.append("task missing title")
        if task.status not in {"todo", "doing", "blocked", "done"}:
            issues.append(f"invalid status: {task.status}")
    return issues
