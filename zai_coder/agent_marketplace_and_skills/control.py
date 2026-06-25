"""Marketplace control helpers."""

from __future__ import annotations

from .catalog import skill_catalog, agent_catalog, search_catalog
from .install_policy import install_policy_decision, enable_policy_decision
from .store import MarketplaceStore


def marketplace_status() -> dict:
    return {
        "ok": True,
        "systems": [
            "agent_catalog",
            "skill_catalog",
            "skill_manifest_validator",
            "install_enable_policy",
            "tenant_skill_permissions",
            "compatibility_checks",
            "marketplace_dashboard",
            "review_audit_flow",
            "offline_import_export",
            "skill_pack_builder",
        ],
    }


def install_skill_demo(db_path: str = "data/agent-marketplace.db") -> dict:
    policy = install_policy_decision("repo-planner", "builder", ("tenant_admin",), True, "", False)
    if not policy["allowed"]:
        return {"ok": False, "policy": policy}
    store = MarketplaceStore(db_path)
    installation = store.install_skill("repo-planner", "org_local", "ws_default", "admin", False)
    audit = store.audit("org_local", "ws_default", "admin", "skill.installed", "repo-planner", installation.to_dict())
    return {"ok": True, "installation": installation.to_dict(), "audit": audit.to_dict()}


def enable_skill_demo(db_path: str = "data/agent-marketplace.db") -> dict:
    policy = enable_policy_decision("repo-planner", ("tenant_admin",), "approved_manual_001")
    if not policy["allowed"]:
        return {"ok": False, "policy": policy}
    store = MarketplaceStore(db_path)
    installation = store.install_skill("repo-planner", "org_local", "ws_default", "admin", False)
    store.set_enabled(installation.id, True)
    audit = store.audit("org_local", "ws_default", "admin", "skill.enabled", "repo-planner", {"installation_id": installation.id})
    return {"ok": True, "installation_id": installation.id, "audit": audit.to_dict()}


def marketplace_overview() -> dict:
    return {"skills": skill_catalog(), "agents": agent_catalog(), "search_demo": search_catalog("release")}
