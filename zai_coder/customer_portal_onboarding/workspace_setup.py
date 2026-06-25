"""Workspace setup and provisioning plans."""

from __future__ import annotations


def workspace_setup_plan(org_id: str = "org_demo", workspace_id: str = "ws_demo") -> dict:
    return {
        "dry_run": True,
        "org_id": org_id,
        "workspace_id": workspace_id,
        "provision": False,
        "steps": [
            "create workspace record draft",
            "assign owner role",
            "apply default quota profile",
            "enable free-plan customer portal features",
            "prepare onboarding checklist",
            "write audit event",
        ],
    }


def workspace_setup_gate(plan: dict, approval_id: str = "", apply_requested: bool = False) -> dict:
    blocked = []
    if apply_requested:
        blocked.append("workspace provisioning is disabled by this package")
    if not plan.get("dry_run", True):
        blocked.append("workspace setup plan must remain dry-run")
    if approval_id and not approval_id.startswith("approved_"):
        blocked.append("invalid approval id")
    return {"allowed": not blocked, "blocked": blocked, "plan": plan}
