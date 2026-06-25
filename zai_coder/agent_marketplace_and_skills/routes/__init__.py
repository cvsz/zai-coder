"""Agent Marketplace and Skills route registry."""

from __future__ import annotations

from zai_coder.agent_marketplace_and_skills.control import marketplace_status, marketplace_overview, install_skill_demo, enable_skill_demo
from zai_coder.agent_marketplace_and_skills.catalog import skill_catalog, agent_catalog, search_catalog
from zai_coder.agent_marketplace_and_skills.validator import validate_skill_manifest_payload, manifest_security_report
from zai_coder.agent_marketplace_and_skills.catalog import find_skill
from zai_coder.agent_marketplace_and_skills.compatibility import compatibility_decision, agent_default_skill_plan
from zai_coder.agent_marketplace_and_skills.permissions import skill_permission_decision
from zai_coder.agent_marketplace_and_skills.install_policy import install_policy_decision, enable_policy_decision
from zai_coder.agent_marketplace_and_skills.store import MarketplaceStore
from zai_coder.agent_marketplace_and_skills.import_export import export_marketplace_bundle, validate_import_bundle
from zai_coder.agent_marketplace_and_skills.pack_builder import skill_pack_plan, build_skill_pack
from zai_coder.agent_marketplace_and_skills.ui.pages import render_marketplace_overview, render_skills_page, render_agents_page, render_policy_page


def route_marketplace_status() -> dict:
    return {
        "ok": True,
        "service": "zai-agent-marketplace-and-skills",
        "systems": [
            "agent_catalog",
            "skill_catalog",
            "skill_manifest_validator",
            "install_enable_policy",
            "tenant_scoped_skill_permissions",
            "compatibility_checks",
            "marketplace_dashboard",
            "review_audit_flow",
            "offline_import_export",
            "skill_pack_builder",
        ],
    }


def route_marketplace_overview() -> dict:
    return marketplace_overview()


def route_skill_catalog() -> dict:
    return {"skills": skill_catalog()}


def route_agent_catalog() -> dict:
    return {"agents": agent_catalog()}


def route_marketplace_search(query: str = "release") -> dict:
    return search_catalog(query)


def route_skill_validate_demo() -> dict:
    payload = find_skill("repo-planner").to_dict()
    return validate_skill_manifest_payload(payload)


def route_skill_security_report(skill_id: str = "repo-planner") -> dict:
    return manifest_security_report(find_skill(skill_id))


def route_skill_compatibility(agent_type: str = "builder", skill_id: str = "repo-planner") -> dict:
    return compatibility_decision(agent_type, skill_id)


def route_agent_default_skill_plan(agent_id: str = "builder-agent") -> dict:
    return agent_default_skill_plan(agent_id)


def route_skill_permission_decision() -> dict:
    return skill_permission_decision(("tenant_admin",), ("skill:view", "skill:install"))


def route_skill_install_policy(skill_id: str = "repo-planner", agent_type: str = "builder") -> dict:
    return install_policy_decision(skill_id, agent_type)


def route_skill_enable_policy(skill_id: str = "repo-planner") -> dict:
    return enable_policy_decision(skill_id)


def route_skill_install_demo() -> dict:
    return install_skill_demo()


def route_skill_enable_demo() -> dict:
    return enable_skill_demo()


def route_marketplace_audit() -> dict:
    return {"events": MarketplaceStore().list_audit("org_local")}


def route_skill_review_demo() -> dict:
    review = MarketplaceStore().add_review("repo-planner", "admin", 5, "Useful safe planning skill.")
    return review.to_dict()


def route_marketplace_export() -> dict:
    return {"path": export_marketplace_bundle(".")}


def route_marketplace_import_validate() -> dict:
    payload = {"offline": True, "skills": skill_catalog(), "agents": agent_catalog()}
    return validate_import_bundle(payload)


def route_skill_pack_plan() -> dict:
    return skill_pack_plan(["repo-planner", "release-checker"])


def route_skill_pack_build() -> dict:
    return {"path": build_skill_pack(["repo-planner", "release-checker"])}


def route_marketplace_page() -> dict:
    return {"content_type": "text/html", "html": render_marketplace_overview()}


def route_marketplace_skills_page() -> dict:
    return {"content_type": "text/html", "html": render_skills_page()}


def route_marketplace_agents_page() -> dict:
    return {"content_type": "text/html", "html": render_agents_page()}


def route_marketplace_policy_page() -> dict:
    return {"content_type": "text/html", "html": render_policy_page()}
