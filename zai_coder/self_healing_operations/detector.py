"""Incident detection rules."""

from __future__ import annotations

import uuid

from .models import Incident, HealthSignal
from .signals import signal_summary, create_signal


def fetch_real_system_signals(service: str = "core") -> list[HealthSignal]:
    import os
    import psutil
    signals = []
    
    # Disk Usage
    try:
        disk_usage = psutil.disk_usage("/")
        disk_ratio = disk_usage.percent / 100.0
        signals.append(create_signal("psutil_disk", "disk_usage_ratio", disk_ratio, service=service))
    except Exception:
        pass

    # CPU or memory could be added too
    try:
        mem_usage = psutil.virtual_memory()
        mem_ratio = mem_usage.percent / 100.0
        # If we had a threshold for mem_ratio, we'd use it. Let's just pass disk for now to match DEFAULT_THRESHOLDS
    except Exception:
        pass

    return signals


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


def detect_incident(signals: list[HealthSignal] | None = None, service: str = "core", execute: bool = False) -> dict:
    if signals is None:
        signals = []
    
    if execute:
        # Fetch real signals from the system
        signals.extend(fetch_real_system_signals(service=service))

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
