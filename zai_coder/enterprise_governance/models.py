"""Enterprise governance models."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass(frozen=True)
class GovernancePolicy:
    id: str
    name: str
    description: str
    severity: str = "medium"
    required: bool = True
    controls: tuple[str, ...] = ()
    created_at: str = field(default_factory=now_iso)

    def validate(self) -> list[str]:
        issues: list[str] = []
        if not self.id:
            issues.append("policy id required")
        if not self.name:
            issues.append("policy name required")
        if self.severity not in {"low", "medium", "high", "critical"}:
            issues.append("invalid severity")
        return issues

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "severity": self.severity,
            "required": self.required,
            "controls": list(self.controls),
            "created_at": self.created_at,
        }


@dataclass(frozen=True)
class GovernanceDecision:
    allowed: bool
    policy_id: str
    reason: str
    severity: str = "medium"
    evidence_required: bool = False

    def to_dict(self) -> dict:
        return {
            "allowed": self.allowed,
            "policy_id": self.policy_id,
            "reason": self.reason,
            "severity": self.severity,
            "evidence_required": self.evidence_required,
        }


@dataclass(frozen=True)
class RiskItem:
    id: str
    title: str
    category: str
    likelihood: int
    impact: int
    mitigation: str
    owner: str = "platform-owner"
    status: str = "open"

    @property
    def score(self) -> int:
        return self.likelihood * self.impact

    def validate(self) -> list[str]:
        issues = []
        if not self.id or not self.title:
            issues.append("risk id and title required")
        if not (1 <= self.likelihood <= 5):
            issues.append("likelihood must be 1..5")
        if not (1 <= self.impact <= 5):
            issues.append("impact must be 1..5")
        if self.status not in {"open", "mitigating", "accepted", "closed"}:
            issues.append("invalid status")
        return issues

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "category": self.category,
            "likelihood": self.likelihood,
            "impact": self.impact,
            "score": self.score,
            "mitigation": self.mitigation,
            "owner": self.owner,
            "status": self.status,
        }


@dataclass(frozen=True)
class EvidenceItem:
    id: str
    control: str
    source: str
    summary: str
    path: str = ""
    collected_at: str = field(default_factory=now_iso)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "control": self.control,
            "source": self.source,
            "summary": self.summary,
            "path": self.path,
            "collected_at": self.collected_at,
        }


@dataclass(frozen=True)
class ChangeRequest:
    id: str
    title: str
    requester: str
    risk_level: str
    target: str
    status: str = "pending"
    approvals: tuple[str, ...] = ()
    created_at: str = field(default_factory=now_iso)

    def validate(self) -> list[str]:
        issues = []
        if self.risk_level not in {"low", "medium", "high", "critical"}:
            issues.append("invalid risk level")
        if self.status not in {"pending", "approved", "rejected", "implemented", "rolled_back"}:
            issues.append("invalid status")
        return issues

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "requester": self.requester,
            "risk_level": self.risk_level,
            "target": self.target,
            "status": self.status,
            "approvals": list(self.approvals),
            "created_at": self.created_at,
        }
