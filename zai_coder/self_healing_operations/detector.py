"""Incident detection rules."""

from __future__ import annotations

import uuid

from .models import Incident, HealthSignal
from .signals import signal_summary


def severity_from_signals(signals: list[HealthSignal]) -> str:
    summary = signal_summary(signals)
    critical = summary["counts"].get("critical", 0)
    warning = summary["counts"].get("warning", 0)
    if critical >= 2:
        return "critical"
    if critical == 1:
        return "high"
    if warning >= 2:
        return "medium"
    if warning == 1:
        return "low"
    return "low"


def detect_incident(signals: list[HealthSignal], service: str = "core") -> dict:
    actionable = [signal for signal in signals if signal.status in {"warning", "critical"}]
    if not actionable:
        return {"detected": False, "summary": signal_summary(signals)}
    severity = severity_from_signals(actionable)
    incident = Incident(
        id=f"inc_{uuid.uuid4().hex[:12]}",
        title=f"{service} health degradation detected",
        severity=severity,
        service=service,
        signals=tuple(signal.to_dict() for signal in actionable),
    )
    issues = incident.validate()
    if issues:
        raise ValueError("; ".join(issues))
    return {"detected": True, "incident": incident.to_dict(), "summary": signal_summary(signals)}


def incident_triage_plan(incident: dict) -> dict:
    return {
        "dry_run": True,
        "incident_id": incident["id"],
        "severity": incident["severity"],
        "steps": [
            "freeze risky automation",
            "collect latest health signals",
            "check recent release/update events",
            "check worker and agent queues",
            "select safe remediation playbook",
            "prepare rollback plan",
            "escalate if severity high or critical",
        ],
    }
