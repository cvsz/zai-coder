"""Agent crash recovery planning."""

from __future__ import annotations


def crash_recovery_plan(agent: dict, reason: str = "heartbeat_stale") -> dict:
    return {
        "dry_run": True,
        "agent_id": agent.get("id"),
        "reason": reason,
        "steps": [
            "mark agent crashed",
            "capture latest heartbeat",
            "capture assigned/running tasks",
            "write audit event",
            "check recovery budget",
            "enqueue recovery worker job",
            "restart only after lifecycle gate passes",
        ],
        "safe_mode": True,
    }


def recovery_allowed(agent: dict, crash_count_24h: int = 0, max_restarts_24h: int = 3) -> dict:
    allowed = crash_count_24h < max_restarts_24h and agent.get("status") in {"crashed", "starting", "running"}
    return {
        "allowed": allowed,
        "crash_count_24h": crash_count_24h,
        "max_restarts_24h": max_restarts_24h,
        "reason": "restart budget available" if allowed else "restart budget exhausted or invalid status",
    }
