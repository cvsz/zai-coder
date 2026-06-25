"""Storyboard and shot list primitives."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass
class Shot:
    scene_slug: str
    shot_type: str
    description: str
    duration_seconds: float = 5.0

    def to_dict(self) -> dict:
        return {
            "scene_slug": self.scene_slug,
            "shot_type": self.shot_type,
            "description": self.description,
            "duration_seconds": self.duration_seconds,
        }


def validate_shots(shots: List[Shot]) -> list[str]:
    issues: list[str] = []
    for i, shot in enumerate(shots, start=1):
        if not shot.scene_slug:
            issues.append(f"shot {i}: missing scene slug")
        if not shot.description:
            issues.append(f"shot {i}: missing description")
        if shot.duration_seconds <= 0:
            issues.append(f"shot {i}: invalid duration")
    return issues


def render_shotlist(shots: List[Shot]) -> str:
    lines = ["# Shot List", ""]
    for i, shot in enumerate(shots, start=1):
        lines.append(f"{i}. `{shot.scene_slug}` [{shot.shot_type}] {shot.description} ({shot.duration_seconds}s)")
    return "\n".join(lines).rstrip() + "\n"
