"""Healing plan builder."""

from __future__ import annotations

import uuid
from pathlib import Path
import json

from .models import HealingPlan
from .playbooks import match_playbook, find_playbook
from .guardrails import auto_heal_gate, rollback_guard


def build_healing_plan(incident: dict, approval_id: str = "", within_maintenance_window: bool = False) -> dict:
    signals = incident.get("signals", [])
    trigger = signals[0].get("metric", "heartbeat_age_seconds") if signals else "heartbeat_age_seconds"
    playbook = match_playbook(incident.get("service", "core"), trigger)
    rollback = (
        "capture current service state",
        "restore previous known-good config/package",
        "run healthcheck",
        "write healing audit event",
    )
    plan = HealingPlan(
        id=f"heal_{uuid.uuid4().hex[:12]}",
        incident_id=incident["id"],
        playbook_id=playbook.id,
        actions=playbook.actions,
        approval_id=approval_id,
        rollback_plan=rollback,
    )
    issues = plan.validate()
    if issues:
        raise ValueError("; ".join(issues))
    gate = auto_heal_gate(playbook.to_dict(), incident["severity"], approval_id, within_maintenance_window)
    rollback = rollback_guard(plan.rollback_plan, backup_ready=True, smoke_tests_defined=True)
    return {"plan": plan.to_dict(), "gate": gate, "rollback": rollback}


def write_healing_plan(plan: dict, root: str | Path = ".", out_dir: str = "healing/plans") -> str:
    root = Path(root)
    path = root / out_dir / f"{plan['id']}.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(plan, indent=2, sort_keys=True), encoding="utf-8")
    return str(path)


def healing_readiness(plan_payload: dict, approval_id: str = "", apply_requested: bool = False) -> dict:
    blocked = []
    if apply_requested:
        blocked.append("automatic apply is disabled; use approved execution runner manually")
    if not plan_payload.get("dry_run", True):
        blocked.append("plan must stay dry-run")
    if not plan_payload.get("rollback_plan"):
        blocked.append("rollback plan required")
    if approval_id and not approval_id.startswith("approved_"):
        blocked.append("invalid approval id")
    return {"allowed": not blocked, "blocked": blocked, "plan": plan_payload}
