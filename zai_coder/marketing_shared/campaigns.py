"""Marketing shared campaign primitives."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from typing import List


@dataclass
class Campaign:
    slug: str
    name: str
    objective: str
    audience: str
    channels: List[str] = field(default_factory=list)
    status: str = "draft"

    def to_dict(self) -> dict:
        return {
            "slug": self.slug,
            "name": self.name,
            "objective": self.objective,
            "audience": self.audience,
            "channels": list(self.channels),
            "status": self.status,
        }


def validate_campaign(campaign: Campaign) -> list[str]:
    issues: list[str] = []
    if not campaign.slug:
        issues.append("missing slug")
    if not campaign.objective:
        issues.append("missing objective")
    if not campaign.audience:
        issues.append("missing audience")
    if not campaign.channels:
        issues.append("missing channels")
    return issues
