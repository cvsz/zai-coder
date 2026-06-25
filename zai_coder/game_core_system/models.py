"""Game core project models."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List


@dataclass
class GameAsset:
    path: str
    kind: str
    tags: List[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {"path": self.path, "kind": self.kind, "tags": list(self.tags)}


@dataclass
class GameScene:
    slug: str
    title: str
    objective: str
    entities: List[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "slug": self.slug,
            "title": self.title,
            "objective": self.objective,
            "entities": list(self.entities),
        }


@dataclass
class GameProject:
    slug: str
    title: str
    genre: str
    platform: str
    scenes: List[GameScene] = field(default_factory=list)
    assets: List[GameAsset] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "slug": self.slug,
            "title": self.title,
            "genre": self.genre,
            "platform": self.platform,
            "scenes": [s.to_dict() for s in self.scenes],
            "assets": [a.to_dict() for a in self.assets],
        }
