"""Unified creative project types."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List


CREATIVE_PROJECT_TYPES = {
    "game": "Game project",
    "document": "Document project",
    "movie": "Movie project",
    "marketing": "Marketing campaign",
    "social": "Social media plan",
}


@dataclass
class CreativeProject:
    slug: str
    title: str
    project_type: str
    owner: str = ""
    status: str = "draft"
    metadata: Dict[str, str] = field(default_factory=dict)

    def validate(self) -> list[str]:
        issues: list[str] = []
        if not self.slug:
            issues.append("missing slug")
        if not self.title:
            issues.append("missing title")
        if self.project_type not in CREATIVE_PROJECT_TYPES:
            issues.append(f"invalid project_type: {self.project_type}")
        if self.status not in {"draft", "review", "approved", "active", "archived"}:
            issues.append(f"invalid status: {self.status}")
        return issues

    def to_dict(self) -> dict:
        return {
            "slug": self.slug,
            "title": self.title,
            "project_type": self.project_type,
            "owner": self.owner,
            "status": self.status,
            "metadata": dict(self.metadata),
        }
