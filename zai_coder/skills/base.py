from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Skill:
    name: str
    description: str
    safety_notes: list[str]
