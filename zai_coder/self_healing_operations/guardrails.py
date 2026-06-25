"""Self-healing guardrails."""

from __future__ import annotations


FORBIDDEN_ACTION_PATTERNS = ("rm -rf", "drop database", "force push", "--no-verify", "git add .", "git add -a")


def maintenance_window_policy(hour_utc: int = 2, duration_hours: int = 2) -> dict:
    return {
        "window_start_hour_utc": hour_utc,
        "duration_hours": duration_hours,
        "allowed_for_low_risk": True,
        "approval_required_outside_window": True,
        "critical_incident_override_requires_approval": True,
    }


def action_guard(actions: tuple[str, ...] | list[str]) -> dict:
    blocked = []
    for action in actions:
        lower = action.lower()
        for pattern in FORBIDDEN_ACTION_PATTERNS:
            if pattern in lower:
                blocked.append({"action": action, "reason": f"forbidden pattern: {pattern}"})
    return {"allowed": not blocked, "blocked": blocked}


def auto_heal_gate(playbook: dict, severity: str, approval_id: str = "", within_maintenance_window: bool = False) -> dict:
    guard = action_guard(playbook.get("actions", []))
    blocked = []
    if not guard["allowed"]:
        blocked.append("forbidden remediation action")
    if playbook.get("risk_level") == "high" and not approval_id.startswith("approved_"):
        blocked.append("high-risk playbook requires approval")
    if severity in {"high", "critical"} and not approval_id.startswith("approved_"):
        blocked.append("high/critical incident requires approval")
    if not within_maintenance_window and not approval_id.startswith("approved_"):
        blocked.append("outside maintenance window requires approval")
    return {
        "allowed": not blocked,
        "blocked": blocked,
        "action_guard": guard,
        "playbook": playbook,
        "severity": severity,
        "within_maintenance_window": within_maintenance_window,
    }


def rollback_guard(rollback_plan: list[str] | tuple[str, ...], backup_ready: bool, smoke_tests_defined: bool) -> dict:
    checks = {
        "rollback_plan_present": bool(rollback_plan),
        "backup_ready": backup_ready,
        "smoke_tests_defined": smoke_tests_defined,
    }
    blocked = [key for key, ok in checks.items() if not ok]
    return {"allowed": not blocked, "blocked": blocked, "checks": checks}
