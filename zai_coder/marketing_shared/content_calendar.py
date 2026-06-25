"""Content calendar planner for marketing shared system."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import List


@dataclass
class ContentItem:
    title: str
    channel: str
    publish_date: str
    status: str = "draft"
    owner: str = ""

    def to_dict(self) -> dict:
        return {
            "title": self.title,
            "channel": self.channel,
            "publish_date": self.publish_date,
            "status": self.status,
            "owner": self.owner,
        }


def validate_calendar(items: List[ContentItem]) -> list[str]:
    issues: list[str] = []
    seen = set()
    for item in items:
        key = (item.channel, item.publish_date, item.title)
        if key in seen:
            issues.append(f"duplicate content item: {item.title}")
        seen.add(key)
        if not item.channel:
            issues.append(f"missing channel: {item.title}")
        if item.status not in {"draft", "review", "approved", "scheduled", "published"}:
            issues.append(f"invalid status for {item.title}: {item.status}")
    return issues
