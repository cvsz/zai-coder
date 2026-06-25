"""Skill install/enable policy."""

from __future__ import annotations

from .catalog import find_skill
from .compatibility import compatibility_decision
from .permissions import skill_permission_decision


def install_policy_decision(
    skill_id: str,
    agent_type: str,
    roles: tuple[str, ...] = ("tenant_admin",),
    dry_run_completed: bool = True,
    approval_id: str = "",
    enable: bool = False,
) -> dict:
    skill = find_skill(skill_id)
    compatibility = compatibility_decision(agent_type, skill_id)
    permissions = skill_permission_decision(roles, tuple(set(skill.required_permissions) | {"skill:install"}))
    blocked = []
    if not dry_run_completed:
        blocked.append("dry-run required before install")
    if enable and not approval_id.startswith("approved_"):
        blocked.append("enable requires approval_id")
    if not compatibility["allowed"]:
        blocked.append(compatibility["reason"])
    if not permissions["allowed"]:
        blocked.append("missing permissions: " + ",".join(permissions["missing"]))
    return {
        "allowed": not blocked,
        "blocked": blocked,
        "skill": skill.to_dict(),
        "compatibility": compatibility,
        "permissions": permissions,
        "dry_run": True,
    }


def enable_policy_decision(skill_id: str, roles: tuple[str, ...] = ("tenant_admin",), approval_id: str = "approved_manual_001") -> dict:
    skill = find_skill(skill_id)
    permissions = skill_permission_decision(roles, ("skill:enable", *skill.required_permissions))
    blocked = []
    if not approval_id.startswith("approved_"):
        blocked.append("approval required")
    if not permissions["allowed"]:
        blocked.append("missing permissions: " + ",".join(permissions["missing"]))
    return {"allowed": not blocked, "blocked": blocked, "skill": skill.to_dict(), "permissions": permissions}
