"""Feedback and Roadmap Center models.

Feedback and roadmap artifacts are local-first and review-first. This package
does not publish public roadmaps, email customers, or mutate releases
automatically.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass(frozen=True)
class FeedbackItem:
    id: str
    customer_id: str
    title: str
    body: str
    category: str = "feature"
    sentiment: str = "neutral"
    priority_hint: str = "normal"
    status: str = "new"
    source: str = "portal"
    created_at: str = field(default_factory=now_iso)

    def validate(self) -> list[str]:
        issues: list[str] = []
        if not self.id or not self.customer_id or not self.title:
            issues.append("feedback id, customer_id, and title required")
        if self.category not in {"feature", "bug", "integration", "docs", "billing", "support", "compliance"}:
            issues.append("invalid category")
        if self.sentiment not in {"positive", "neutral", "negative"}:
            issues.append("invalid sentiment")
        if self.priority_hint not in {"low", "normal", "high", "urgent"}:
            issues.append("invalid priority_hint")
        if self.status not in {"new", "triaged", "linked", "planned", "closed", "duplicate"}:
            issues.append("invalid status")
        forbidden = {"password", "token", "secret", "credit card", "api key"}
        text = f"{self.title} {self.body}".lower()
        if any(term in text for term in forbidden):
            issues.append("feedback text may contain sensitive material")
        return issues

    def to_dict(self) -> dict:
        return self.__dict__.copy()


@dataclass(frozen=True)
class RoadmapItem:
    id: str
    title: str
    description: str
    theme: str = "platform"
    status: str = "candidate"
    horizon: str = "next"
    visibility: str = "private"
    owner: str = "product"
    linked_feedback: tuple[str, ...] = ()
    created_at: str = field(default_factory=now_iso)

    def validate(self) -> list[str]:
        issues: list[str] = []
        if not self.id or not self.title or not self.description:
            issues.append("roadmap id, title, and description required")
        if self.status not in {"candidate", "planned", "in_progress", "shipped", "deferred", "cancelled"}:
            issues.append("invalid roadmap status")
        if self.horizon not in {"now", "next", "later"}:
            issues.append("invalid roadmap horizon")
        if self.visibility not in {"private", "customer", "public"}:
            issues.append("invalid visibility")
        return issues

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "theme": self.theme,
            "status": self.status,
            "horizon": self.horizon,
            "visibility": self.visibility,
            "owner": self.owner,
            "linked_feedback": list(self.linked_feedback),
            "created_at": self.created_at,
        }


@dataclass(frozen=True)
class PriorityScore:
    id: str
    roadmap_id: str
    reach: int
    impact: int
    confidence: int
    effort: int
    score: float
    method: str = "RICE"

    def validate(self) -> list[str]:
        issues: list[str] = []
        for name, value in {"reach": self.reach, "impact": self.impact, "confidence": self.confidence, "effort": self.effort}.items():
            if value < 1:
                issues.append(f"{name} must be >= 1")
        if self.score < 0:
            issues.append("score must be >= 0")
        if self.method not in {"RICE", "ICE", "WSJF"}:
            issues.append("invalid prioritization method")
        return issues

    def to_dict(self) -> dict:
        return self.__dict__.copy()


@dataclass(frozen=True)
class ReleaseLink:
    id: str
    roadmap_id: str
    target_version: str
    release_channel: str = "stable"
    status: str = "draft"

    def validate(self) -> list[str]:
        issues: list[str] = []
        if not self.id or not self.roadmap_id or not self.target_version:
            issues.append("release link id, roadmap_id, and target_version required")
        if not self.target_version.startswith("v"):
            issues.append("target_version must start with v")
        if self.release_channel not in {"dev", "alpha", "beta", "rc", "stable", "lts"}:
            issues.append("invalid release_channel")
        if self.status not in {"draft", "approved", "released", "rolled_back"}:
            issues.append("invalid release link status")
        return issues

    def to_dict(self) -> dict:
        return self.__dict__.copy()


@dataclass(frozen=True)
class RoadmapAuditEvent:
    id: str
    actor: str
    action: str
    target: str
    payload: dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=now_iso)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "actor": self.actor,
            "action": self.action,
            "target": self.target,
            "payload": dict(self.payload),
            "created_at": self.created_at,
        }
