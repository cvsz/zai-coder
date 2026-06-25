"""Agent budget and permission guard."""

from __future__ import annotations

from .models import AgentBudget


def budget_decision(budget: AgentBudget, usage: dict[str, int]) -> dict:
    issues = budget.validate()
    if issues:
        return {"allowed": False, "reason": "; ".join(issues), "budget": budget.to_dict(), "usage": dict(usage)}
    checks = {
        "tasks": usage.get("tasks", 0) <= budget.max_tasks_per_day,
        "runtime_minutes": usage.get("runtime_minutes", 0) <= budget.max_runtime_minutes_per_day,
        "provider_apply": usage.get("provider_apply", 0) <= budget.max_provider_apply_per_day,
    }
    blocked = [key for key, ok in checks.items() if not ok]
    return {
        "allowed": not blocked,
        "blocked": blocked,
        "checks": checks,
        "budget": budget.to_dict(),
        "usage": dict(usage),
    }


def agent_permission_decision(roles: tuple[str, ...], action: str) -> dict:
    permissions = {
        "agent_owner": {"agent:*"},
        "agent_admin": {"agent:view", "agent:start", "agent:stop", "agent:assign", "agent:recover"},
        "operator": {"agent:view", "agent:assign"},
        "viewer": {"agent:view"},
    }
    allowed_permissions = set()
    for role in roles:
        allowed_permissions.update(permissions.get(role, set()))
    required = f"agent:{action}"
    allowed = "agent:*" in allowed_permissions or required in allowed_permissions
    return {"allowed": allowed, "required": required, "roles": list(roles), "permissions": sorted(allowed_permissions)}
