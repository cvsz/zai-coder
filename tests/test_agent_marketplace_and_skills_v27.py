from pathlib import Path
import tempfile
import json

from zai_coder.agent_marketplace_and_skills.models import SkillManifest, AgentListing, SkillInstallation, SkillReview
from zai_coder.agent_marketplace_and_skills.catalog import skill_catalog, agent_catalog, find_skill, find_agent_listing, search_catalog
from zai_coder.agent_marketplace_and_skills.validator import validate_skill_manifest_payload, manifest_security_report
from zai_coder.agent_marketplace_and_skills.compatibility import compatibility_decision, agent_default_skill_plan
from zai_coder.agent_marketplace_and_skills.permissions import permissions_for_roles, skill_permission_decision
from zai_coder.agent_marketplace_and_skills.install_policy import install_policy_decision, enable_policy_decision
from zai_coder.agent_marketplace_and_skills.store import MarketplaceStore
from zai_coder.agent_marketplace_and_skills.import_export import export_marketplace_bundle, validate_import_bundle
from zai_coder.agent_marketplace_and_skills.pack_builder import build_skill_pack, skill_pack_plan
from zai_coder.agent_marketplace_and_skills.control import marketplace_status, install_skill_demo, enable_skill_demo, marketplace_overview
from zai_coder.agent_marketplace_and_skills.ui.pages import render_marketplace_overview, render_skills_page, render_agents_page, render_policy_page
from zai_coder.agent_marketplace_and_skills.routes import (
    route_marketplace_status,
    route_marketplace_overview,
    route_skill_catalog,
    route_agent_catalog,
    route_marketplace_search,
    route_skill_validate_demo,
    route_skill_security_report,
    route_skill_compatibility,
    route_agent_default_skill_plan,
    route_skill_permission_decision,
    route_skill_install_policy,
    route_skill_enable_policy,
    route_skill_install_demo,
    route_skill_enable_demo,
    route_marketplace_audit,
    route_skill_review_demo,
    route_marketplace_export,
    route_marketplace_import_validate,
    route_skill_pack_plan,
    route_skill_pack_build,
    route_marketplace_page,
    route_marketplace_skills_page,
    route_marketplace_agents_page,
    route_marketplace_policy_page,
)


def test_models_validation():
    assert SkillManifest("s", "Skill", "1.0.0", "desc").validate() == []
    assert SkillManifest("../bad", "", "", "desc", entrypoint="run.py").validate()
    assert AgentListing("a", "Agent", "builder", "desc").validate() == []
    assert AgentListing("../bad", "", "", "", status="bad").validate()
    assert SkillInstallation("i", "s", "org", "ws").validate() == []
    assert SkillReview("r", "s", "reviewer", 5, "nice").validate() == []
    assert SkillReview("", "", "", 9, "x").validate()


def test_catalog_validator_security():
    assert skill_catalog()
    assert agent_catalog()
    assert find_skill("repo-planner").name == "Repository Planner"
    assert find_agent_listing("builder-agent").agent_type == "builder"
    assert search_catalog("release")["skills"]
    payload = find_skill("repo-planner").to_dict()
    assert validate_skill_manifest_payload(payload)["ok"] is True
    risky = SkillManifest("risky", "Risky", "1.0.0", "desc", required_permissions=("providers:apply",))
    assert manifest_security_report(risky)["ok"] is False


def test_compat_permissions_policies():
    assert compatibility_decision("builder", "repo-planner")["allowed"] is True
    assert compatibility_decision("builder", "cloudflare-operator")["allowed"] is False
    assert agent_default_skill_plan("builder-agent")["allowed"] is True
    assert "skill:install" in permissions_for_roles(("tenant_admin",))
    assert skill_permission_decision(("viewer",), ("skill:view",))["allowed"] is True
    assert skill_permission_decision(("viewer",), ("skill:install",))["allowed"] is False
    assert install_policy_decision("repo-planner", "builder")["allowed"] is True
    assert install_policy_decision("repo-planner", "builder", dry_run_completed=False)["allowed"] is False
    assert enable_policy_decision("repo-planner", approval_id="approved_manual_001")["allowed"] is True
    assert enable_policy_decision("repo-planner", approval_id="")["allowed"] is False


def test_store_import_export_pack_and_control(tmp_path):
    store = MarketplaceStore(tmp_path / "market.db")
    inst = store.install_skill("repo-planner", "org", "ws", "admin", False)
    assert inst.id.startswith("inst_")
    store.set_enabled(inst.id, True)
    assert store.list_installations("org", "ws")[0]["enabled"] is True
    event = store.audit("org", "ws", "admin", "skill.installed", "repo-planner")
    assert store.list_audit("org")[0]["id"] == event.id
    review = store.add_review("repo-planner", "admin", 5, "good")
    assert store.list_reviews("repo-planner")[0]["id"] == review.id
    bundle_path = export_marketplace_bundle(tmp_path)
    payload = json.loads(Path(bundle_path).read_text())
    assert validate_import_bundle(payload)["ok"] is True
    assert skill_pack_plan(["repo-planner"])["dry_run"] is True
    pack_path = build_skill_pack(["repo-planner"], tmp_path)
    assert Path(pack_path).exists()
    assert marketplace_status()["ok"] is True
    assert install_skill_demo(str(tmp_path / "market2.db"))["ok"] is True
    assert enable_skill_demo(str(tmp_path / "market3.db"))["ok"] is True
    assert marketplace_overview()["skills"]


def test_ui_pages():
    assert "Agent Marketplace and Skills" in render_marketplace_overview()
    assert "Skills" in render_skills_page()
    assert "Agents" in render_agents_page()
    assert "Policy" in render_policy_page()


def test_routes(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    assert route_marketplace_status()["ok"] is True
    assert route_marketplace_overview()["skills"]
    assert route_skill_catalog()["skills"]
    assert route_agent_catalog()["agents"]
    assert route_marketplace_search("release")["skills"]
    assert route_skill_validate_demo()["ok"] is True
    assert route_skill_security_report("repo-planner")["ok"] is True
    assert route_skill_compatibility("builder", "repo-planner")["allowed"] is True
    assert route_agent_default_skill_plan("builder-agent")["allowed"] is True
    assert route_skill_permission_decision()["allowed"] is True
    assert route_skill_install_policy("repo-planner", "builder")["allowed"] is True
    assert route_skill_enable_policy("repo-planner")["allowed"] is True
    assert route_skill_install_demo()["ok"] is True
    assert route_skill_enable_demo()["ok"] is True
    assert "events" in route_marketplace_audit()
    assert route_skill_review_demo()["rating"] == 5
    assert Path(route_marketplace_export()["path"]).exists()
    assert route_marketplace_import_validate()["ok"] is True
    assert route_skill_pack_plan()["dry_run"] is True
    assert Path(route_skill_pack_build()["path"]).exists()
    assert route_marketplace_page()["content_type"] == "text/html"
    assert route_marketplace_skills_page()["content_type"] == "text/html"
    assert route_marketplace_agents_page()["content_type"] == "text/html"
    assert route_marketplace_policy_page()["content_type"] == "text/html"


def test_docs_scripts_assets_exist():
    root = Path(__file__).resolve().parents[1]
    for rel in [
        "scripts/marketplace/marketplace-status.sh",
        "scripts/marketplace/skill-catalog.sh",
        "scripts/marketplace/marketplace-search.sh",
        "scripts/marketplace/skill-validate.sh",
        "scripts/marketplace/skill-compatibility.sh",
        "scripts/marketplace/skill-install-policy.sh",
        "scripts/marketplace/skill-install-demo.sh",
        "scripts/marketplace/skill-enable-demo.sh",
        "scripts/marketplace/marketplace-audit.sh",
        "scripts/marketplace/skill-review-demo.sh",
        "scripts/marketplace/marketplace-export.sh",
        "scripts/marketplace/skill-pack-build.sh",
        "scripts/marketplace/marketplace-dashboard-export.sh",
        "docs/marketplace/AGENT_MARKETPLACE_AND_SKILLS_GUIDE.md",
        "docs/marketplace/SKILL_MANIFEST.md",
        "docs/marketplace/SKILL_INSTALL_POLICY.md",
        "docs/marketplace/AGENT_SKILL_COMPATIBILITY.md",
        "docs/marketplace/MARKETPLACE_IMPORT_EXPORT.md",
        "docs/marketplace/SKILL_PACK_BUILDER.md",
        "docs/requirements/NEXT_V27_AGENT_MARKETPLACE_AND_SKILLS_REQUIREMENTS.md",
        "assets/marketplace/agent_marketplace_and_skills_features.json",
    ]:
        assert (root / rel).exists(), rel
