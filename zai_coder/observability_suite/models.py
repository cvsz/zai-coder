"""Observability suite models."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass(frozen=True)
class MetricSample:
    name: str
    value: float
    kind: str = "gauge"
    labels: dict[str, str] = field(default_factory=dict)
    ts: str = field(default_factory=now_iso)

    def validate(self) -> list[str]:
        issues: list[str] = []
        if not self.name:
            issues.append("metric name required")
        if self.kind not in {"counter", "gauge", "histogram"}:
            issues.append(f"invalid metric kind: {self.kind}")
        if any(not k or not v for k, v in self.labels.items()):
            issues.append("labels must be non-empty strings")
        return issues

    def to_dict(self) -> dict:
        return {"name": self.name, "value": self.value, "kind": self.kind, "labels": dict(self.labels), "ts": self.ts}


@dataclass(frozen=True)
class StructuredEvent:
    topic: str
    level: str
    message: str
    payload: dict[str, Any] = field(default_factory=dict)
    ts: str = field(default_factory=now_iso)

    def validate(self) -> list[str]:
        issues = []
        if not self.topic:
            issues.append("topic required")
        if self.level not in {"debug", "info", "warning", "error", "critical"}:
            issues.append(f"invalid level: {self.level}")
        if not self.message:
            issues.append("message required")
        return issues

    def to_dict(self) -> dict:
        return {"topic": self.topic, "level": self.level, "message": self.message, "payload": dict(self.payload), "ts": self.ts}


@dataclass(frozen=True)
class AlertRule:
    name: str
    metric: str
    operator: str
    threshold: float
    severity: str = "warning"
    duration_seconds: int = 60

    def evaluate(self, value: float) -> bool:
        if self.operator == ">":
            return value > self.threshold
        if self.operator == ">=":
            return value >= self.threshold
        if self.operator == "<":
            return value < self.threshold
        if self.operator == "<=":
            return value <= self.threshold
        if self.operator == "==":
            return value == self.threshold
        raise ValueError(f"unsupported operator: {self.operator}")

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "metric": self.metric,
            "operator": self.operator,
            "threshold": self.threshold,
            "severity": self.severity,
            "duration_seconds": self.duration_seconds,
        }
