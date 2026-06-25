"""Self-Healing Operations route registry."""

from __future__ import annotations

from zai_coder.self_healing_operations.control import self_healing_status, self_healing_overview, incident_demo, healing_plan_demo
from zai_coder.self_healing_operations.signals import create_signal, signal_summary
from zai_coder.self_healing_operations.playbooks import playbook_catalog, validate_playbook_catalog
from zai_coder.self_healing_operations.guardrails import maintenance_window_policy, action_guard, auto_heal_gate, rollback_guard
from zai_coder.self_healing_operations.escalation import escalation_policy, escalation_decision, notification_draft
from zai_coder.self_healing_operations.postmortem import postmortem_markdown
from zai_coder.self_healing_operations.audit import HealingAuditLog
from zai_coder.self_healing_operations.ui.pages import render_healing_overview, render_incidents_page, render_playbooks_page, render_policy_page


def route_self_healing_status() -> dict:
    return {
        "ok": True,
        "service": "zai-self-healing-operations",
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


def route_self_healing_overview() -> dict:
    return self_healing_overview()


def route_signal_demo() -> dict:
    signals = [
        create_signal("gateway", "error_rate", 0.06, "core"),
        create_signal("workers", "queue_depth", 250, "workers"),
    ]
    return signal_summary(signals)


def route_incident_demo() -> dict:
    return incident_demo()


def route_playbook_catalog() -> dict:
    return {"playbooks": playbook_catalog(), "validation": validate_playbook_catalog()}


def route_guardrail_policy() -> dict:
    return {
        "maintenance": maintenance_window_policy(),
        "action_guard": action_guard(["make healthcheck", "make deploy-systemd"]),
        "rollback": rollback_guard(["restore previous package"], True, True),
    }


def route_healing_plan_demo() -> dict:
    return healing_plan_demo(".")


def route_escalation_demo() -> dict:
    incident = incident_demo()["incident"]
    return {"decision": escalation_decision(incident), "notification": notification_draft(incident)}


def route_postmortem_demo() -> dict:
    incident = incident_demo()["incident"]
    return {"markdown": postmortem_markdown(incident)}


def route_healing_audit() -> dict:
    return {"events": HealingAuditLog().list_events()}


def route_self_healing_page() -> dict:
    return {"content_type": "text/html", "html": render_healing_overview()}


def route_self_healing_incidents_page() -> dict:
    return {"content_type": "text/html", "html": render_incidents_page()}


def route_self_healing_playbooks_page() -> dict:
    return {"content_type": "text/html", "html": render_playbooks_page()}


def route_self_healing_policy_page() -> dict:
    return {"content_type": "text/html", "html": render_policy_page()}
