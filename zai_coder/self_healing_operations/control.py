"""Self-healing operations control helpers."""

from __future__ import annotations

from .signals import create_signal, signal_summary
from .detector import detect_incident, incident_triage_plan
from .planner import build_healing_plan, write_healing_plan
from .postmortem import write_postmortem
from .audit import HealingAuditLog


def self_healing_status() -> dict:
    return {
        "ok": True,
        "systems": [
            "health_signal_monitor",
            "incident_detector",
            "remediation_playbooks",
            "safe_auto_heal_planner",
            "rollback_guard",
            "maintenance_window_policy",
            "escalation_policy",
            "postmortem_generator",
            "self_healing_dashboard",
            "healing_audit_log",
        ],
    }


def demo_signals() -> list:
    return [
        create_signal("gateway", "error_rate", 0.06, "core"),
        create_signal("workers", "queue_depth", 250, "workers"),
        create_signal("agents", "heartbeat_age_seconds", 120, "agents"),
    ]


def incident_demo() -> dict:
    signals = demo_signals()
    return detect_incident(signals, "core")


def healing_plan_demo(root: str = ".") -> dict:
    detected = incident_demo()
    incident = detected["incident"]
    plan_payload = build_healing_plan(incident, "approved_manual_001", True)
    path = write_healing_plan(plan_payload["plan"], root)
    postmortem = write_postmortem(incident, plan_payload["plan"], root)
    audit = HealingAuditLog().record("system", "healing.plan_created", incident["id"], plan_payload)
    return {"incident": incident, "healing": plan_payload, "plan_path": path, "postmortem_path": postmortem, "audit": audit.to_dict()}


def self_healing_overview() -> dict:
    signals = demo_signals()
    detected = detect_incident(signals, "core")
    triage = incident_triage_plan(detected["incident"]) if detected["detected"] else None
    return {"status": self_healing_status(), "signals": signal_summary(signals), "detected": detected, "triage": triage}
