"""Enterprise Reporting and Board Pack models.

This package generates board-ready reporting artifacts from local scaffold data.
It does not make investor claims automatically, certify financials, or publish
reports externally.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass(frozen=True)
class KPI:
    id: str
    name: str
    value: float
    unit: str
    trend: str = "flat"
    target: float | None = None
    category: str = "operations"

    def validate(self) -> list[str]:
        issues: list[str] = []
        if not self.id or not self.name or not self.unit:
            issues.append("kpi id, name, and unit required")
        if self.trend not in {"up", "down", "flat", "unknown"}:
            issues.append("invalid trend")
        if self.value < 0:
            issues.append("kpi value must be >= 0")
        return issues

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "value": self.value,
            "unit": self.unit,
            "trend": self.trend,
            "target": self.target,
            "category": self.category,
        }


@dataclass(frozen=True)
class BoardDecision:
    id: str
    title: str
    owner: str
    status: str = "proposed"
    decision_type: str = "strategic"
    due_date: str = ""
    context: str = ""

    def validate(self) -> list[str]:
        issues: list[str] = []
        if not self.id or not self.title or not self.owner:
            issues.append("decision id, title, and owner required")
        if self.status not in {"proposed", "approved", "rejected", "deferred", "completed"}:
            issues.append("invalid decision status")
        if self.decision_type not in {"strategic", "financial", "risk", "product", "operations", "compliance"}:
            issues.append("invalid decision type")
        return issues

    def to_dict(self) -> dict:
        return self.__dict__.copy()


@dataclass(frozen=True)
class BoardRisk:
    id: str
    title: str
    severity: str
    owner: str
    mitigation: str
    status: str = "open"

    def validate(self) -> list[str]:
        issues: list[str] = []
        if not self.id or not self.title or not self.owner:
            issues.append("risk id, title, and owner required")
        if self.severity not in {"low", "medium", "high", "critical"}:
            issues.append("invalid severity")
        if self.status not in {"open", "mitigating", "accepted", "closed"}:
            issues.append("invalid risk status")
        if not self.mitigation:
            issues.append("mitigation required")
        return issues

    def to_dict(self) -> dict:
        return self.__dict__.copy()


@dataclass(frozen=True)
class ReportSection:
    id: str
    title: str
    body: str
    order: int = 100
    source: str = "local"

    def validate(self) -> list[str]:
        issues: list[str] = []
        if not self.id or not self.title:
            issues.append("section id and title required")
        if len(self.body) > 50000:
            issues.append("section body too large")
        return issues

    def to_dict(self) -> dict:
        return self.__dict__.copy()


@dataclass(frozen=True)
class BoardPack:
    id: str
    period: str
    title: str
    sections: tuple[dict[str, Any], ...]
    kpis: tuple[dict[str, Any], ...]
    decisions: tuple[dict[str, Any], ...]
    risks: tuple[dict[str, Any], ...]
    dry_run: bool = True
    created_at: str = field(default_factory=now_iso)

    def validate(self) -> list[str]:
        issues: list[str] = []
        if not self.id or not self.period or not self.title:
            issues.append("board pack id, period, and title required")
        if not self.sections:
            issues.append("board pack requires sections")
        if not self.kpis:
            issues.append("board pack requires KPIs")
        if not self.dry_run:
            issues.append("board pack must be dry-run/export-only by default")
        return issues

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "period": self.period,
            "title": self.title,
            "sections": [dict(section) for section in self.sections],
            "kpis": [dict(kpi) for kpi in self.kpis],
            "decisions": [dict(decision) for decision in self.decisions],
            "risks": [dict(risk) for risk in self.risks],
            "dry_run": self.dry_run,
            "created_at": self.created_at,
        }


@dataclass(frozen=True)
class ReportingAuditEvent:
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
