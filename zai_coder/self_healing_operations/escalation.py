"""Escalation policy."""

from __future__ import annotations


def escalation_policy() -> dict:
    return {
        "low": {"notify": ["ops-log"], "page": False, "approval_required": False},
        "medium": {"notify": ["ops-log", "owner"], "page": False, "approval_required": True},
        "high": {"notify": ["ops-log", "owner", "admin"], "page": True, "approval_required": True},
        "critical": {"notify": ["ops-log", "owner", "admin"], "page": True, "approval_required": True},
    }


def escalation_decision(incident: dict) -> dict:
    policy = escalation_policy()[incident["severity"]]
    return {"incident_id": incident["id"], "severity": incident["severity"], "policy": policy, "dry_run": True}


def notification_draft(incident: dict) -> dict:
    return {
        "subject": f"[{incident['severity'].upper()}] {incident['title']}",
        "body": f"Incident {incident['id']} on {incident['service']} requires attention. Status: {incident['status']}.",
        "channels": escalation_policy()[incident["severity"]]["notify"],
        "send": False,
    }
