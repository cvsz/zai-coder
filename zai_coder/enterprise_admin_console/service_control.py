"""Service control panel planning."""

from __future__ import annotations

import uuid

from .models import ServiceActionPlan


SUPPORTED_SERVICES = ("gateway", "workers", "agents", "connectors", "release-center", "self-healing", "compliance", "board-pack")


ACTION_STEPS = {
    "status": ("make healthcheck", "make ops-status-panel"),
    "healthcheck": ("make healthcheck",),
    "restart-plan": ("make healthcheck", "make deploy-systemd", "make healthcheck"),
    "drain-plan": ("make worker-policy", "make worker-lease-and-plan", "make worker-audit"),
    "backup-plan": ("make backup-plan", "make backup-create"),
    "rollback-plan": ("make rollback-migration-gate", "make update-plan"),
}


def service_catalog() -> list[dict]:
    return [{"id": service, "name": service.replace("-", " ").title(), "status": "planned"} for service in SUPPORTED_SERVICES]


def service_action_plan(service: str, action: str = "status") -> ServiceActionPlan:
    if service not in SUPPORTED_SERVICES:
        raise ValueError(f"unknown service: {service}")
    if action not in ACTION_STEPS:
        raise ValueError(f"unknown action: {action}")
    plan = ServiceActionPlan(f"svcplan_{uuid.uuid4().hex[:12]}", service, action, ACTION_STEPS[action])
    issues = plan.validate()
    if issues:
        raise ValueError("; ".join(issues))
    return plan


def service_action_gate(plan: dict, approval_id: str = "", apply_requested: bool = False) -> dict:
    blocked = []
    if apply_requested:
        blocked.append("admin console cannot apply service actions directly")
    read_only_actions = {"status", "healthcheck"}
    if plan.get("approval_required", True) and plan.get("action") not in read_only_actions and not approval_id.startswith("approved_"):
        blocked.append("service action requires approval")
    if not plan.get("dry_run", True):
        blocked.append("service plan must be dry-run")
    return {"allowed": not blocked, "blocked": blocked, "plan": plan}
