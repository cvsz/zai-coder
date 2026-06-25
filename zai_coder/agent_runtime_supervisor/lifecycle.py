"""Agent lifecycle supervisor."""

from __future__ import annotations

VALID_TRANSITIONS = {
    "stopped": {"starting", "terminated"},
    "starting": {"running", "crashed", "stopped"},
    "running": {"paused", "draining", "crashed", "stopped"},
    "paused": {"running", "stopped", "terminated"},
    "draining": {"stopped", "terminated", "crashed"},
    "crashed": {"starting", "terminated"},
    "terminated": set(),
}


def transition_decision(current_status: str, target_status: str) -> dict:
    allowed = target_status in VALID_TRANSITIONS.get(current_status, set())
    return {
        "allowed": allowed,
        "current_status": current_status,
        "target_status": target_status,
        "reason": "transition allowed" if allowed else f"invalid transition: {current_status} -> {target_status}",
    }


def lifecycle_plan(action: str = "start") -> dict:
    plans = {
        "start": ["validate sandbox profile", "check tenant quota", "register runtime", "enqueue worker job", "mark starting", "wait heartbeat", "mark running"],
        "pause": ["mark paused", "stop assigning new tasks", "keep task state"],
        "drain": ["mark draining", "finish current task", "stop leasing new work", "mark stopped"],
        "recover": ["capture crash evidence", "check retry budget", "mark starting", "enqueue recovery job"],
        "terminate": ["cancel queued tasks", "mark terminated", "write audit event"],
    }
    if action not in plans:
        raise ValueError(f"unknown lifecycle action: {action}")
    return {"dry_run": True, "action": action, "steps": plans[action]}
