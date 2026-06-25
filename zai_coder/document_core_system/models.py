"""Document core models."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List


@dataclass
class DocumentSection:
    heading: str
    body: str = ""
    level: int = 2

    def to_markdown(self) -> str:
        level = max(1, min(int(self.level), 6))
        return f"{'#' * level} {self.heading}\n\n{self.body.strip()}\n"


@dataclass
class DocumentProject:
    title: str
    audience: str
    purpose: str
    sections: List[DocumentSection] = field(default_factory=list)
    status: str = "draft"

    def to_dict(self) -> dict:
        return {
            "title": self.title,
            "audience": self.audience,
            "purpose": self.purpose,
            "sections": [{"heading": s.heading, "body": s.body, "level": s.level} for s in self.sections],
            "status": self.status,
        }
