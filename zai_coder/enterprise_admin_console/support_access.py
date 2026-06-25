"""Support access and impersonation guard."""

from __future__ import annotations


def support_access_policy() -> dict:
    return {
        "impersonation_disabled_by_default": True,
        "requires_customer_approval": True,
        "requires_time_bound_session": True,
        "requires_audit_log": True,
        "secrets_redacted": True,
    }


def support_access_gate(actor_roles: tuple[str, ...], target_user: dict, approval_id: str = "", minutes: int = 15) -> dict:
    blocked = []
    if "support_agent" not in actor_roles and "tenant_admin" not in actor_roles and "super_admin" not in actor_roles:
        blocked.append("actor lacks support role")
    if not approval_id.startswith("approved_"):
        blocked.append("support access requires approval")
    if minutes <= 0 or minutes > 60:
        blocked.append("support session must be 1-60 minutes")
    if target_user.get("status") != "active":
        blocked.append("target user must be active")
    return {
        "allowed": not blocked,
        "blocked": blocked,
        "target_user_id": target_user.get("id"),
        "duration_minutes": minutes,
        "policy": support_access_policy(),
    }
