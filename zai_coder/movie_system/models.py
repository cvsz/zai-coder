"""Movie system models for original production planning."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List


@dataclass
class Character:
    name: str
    role: str
    motivation: str = ""

    def to_dict(self) -> dict:
        return {"name": self.name, "role": self.role, "motivation": self.motivation}


@dataclass
class MovieScene:
    slug: str
    location: str
    summary: str
    characters: List[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "slug": self.slug,
            "location": self.location,
            "summary": self.summary,
            "characters": list(self.characters),
        }


@dataclass
class MovieProject:
    title: str
    logline: str
    genre: str
    rating: str = "general"
    characters: List[Character] = field(default_factory=list)
    scenes: List[MovieScene] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "title": self.title,
            "logline": self.logline,
            "genre": self.genre,
            "rating": self.rating,
            "characters": [c.to_dict() for c in self.characters],
            "scenes": [s.to_dict() for s in self.scenes],
        }
