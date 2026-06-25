"""Roadmap prioritization scoring."""

from __future__ import annotations

import uuid

from .models import PriorityScore


def rice_score(reach: int, impact: int, confidence: int, effort: int) -> float:
    if effort <= 0:
        raise ValueError("effort must be > 0")
    return round((reach * impact * confidence) / effort, 2)


def score_roadmap_item(roadmap_id: str, reach: int = 10, impact: int = 3, confidence: int = 8, effort: int = 5) -> PriorityScore:
    score = PriorityScore(
        id=f"prio_{uuid.uuid4().hex[:12]}",
        roadmap_id=roadmap_id,
        reach=reach,
        impact=impact,
        confidence=confidence,
        effort=effort,
        score=rice_score(reach, impact, confidence, effort),
    )
    issues = score.validate()
    if issues:
        raise ValueError("; ".join(issues))
    return score


def prioritization_matrix(roadmap_items: list[dict]) -> dict:
    rows = []
    for idx, item in enumerate(roadmap_items):
        reach = 10 + idx * 5
        impact = 2 + (idx % 3)
        confidence = 7 + (idx % 2)
        effort = 3 + idx
        rows.append(score_roadmap_item(item["id"], reach, impact, confidence, effort).to_dict())
    return {"method": "RICE", "scores": sorted(rows, key=lambda row: row["score"], reverse=True)}
