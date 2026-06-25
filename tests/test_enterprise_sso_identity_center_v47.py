from pathlib import Path
from zai_coder.enterprise_sso_identity_center.models import IdentityProviderPlan, ScimMapping, OrgPolicy, AccessReviewItem
from zai_coder.enterprise_sso_identity_center.core import *
from zai_coder.enterprise_sso_identity_center.routes import *

def test_models_validation():
    assert IdentityProviderPlan("p","Provider","generic_oidc").validate() == []
    assert IdentityProviderPlan("","","bad", protocol="bad", status="bad", dry_run=False).validate()
    assert ScimMapping("m","src","dst").validate() == []
    assert ScimMapping("","","", transform="bad", status="bad").validate()
    assert OrgPolicy("p","Policy","mfa").validate() == []
    assert OrgPolicy("","","bad", enforcement="bad", status="bad").validate()
    assert AccessReviewItem("a","usr","res","viewer").validate() == []
    assert AccessReviewItem("","","","bad", decision="bad", risk="bad").validate()

def test_core_identity():
    assert identity_provider_plans()
    assert scim_mapping_drafts()
    assert org_policy_registry()
    assert access_review_queue()
    assert validation_report()["ok"]
    assert sso_config_plan()["mutate_provider"] is False
    assert scim_mapping_plan()["write_to_idp"] is False
    assert access_review_summary()["apply_changes"] is False
    assert role_assignment_review()["apply_role_change"] is False
    bundle = identity_evidence_bundle()
    assert bundle["external_mutation"] is False
    assert bundle["requires_review"] is True

def test_exports(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    assert Path(write_identity_evidence(tmp_path)).exists()
    assert Path(write_identity_report(tmp_path)).exists()
    demo = identity_demo(str(tmp_path))
    assert Path(demo["evidence_path"]).exists()
    assert Path(demo["report_path"]).exists()

def test_routes():
    assert route_identity_status()["ok"]
    assert route_identity_overview()["validation"]["ok"]
    assert route_sso_plan()["mutate_provider"] is False
    assert route_scim_mapping_draft()["write_to_idp"] is False
    assert route_org_policy()["policies"]
    assert route_access_review()["requires_review"]
    assert route_role_assignment_review()["apply_role_change"] is False
    assert "evidence_path" in route_identity_evidence_export()
    assert "evidence_path" in route_identity_demo()
    assert route_identity_page()["content_type"] == "text/html"
    assert route_identity_sso_page()["content_type"] == "text/html"
    assert route_identity_scim_page()["content_type"] == "text/html"
    assert route_identity_policies_page()["content_type"] == "text/html"
    assert route_identity_access_review_page()["content_type"] == "text/html"

def test_docs_scripts_assets_exist():
    root = Path(__file__).resolve().parents[1]
    for rel in [
        "scripts/identity-center/identity-status.sh",
        "scripts/identity-center/sso-plan.sh",
        "scripts/identity-center/scim-mapping-draft.sh",
        "scripts/identity-center/org-policy.sh",
        "scripts/identity-center/access-review.sh",
        "scripts/identity-center/role-assignment-review.sh",
        "scripts/identity-center/identity-evidence-export.sh",
        "scripts/identity-center/identity-demo.sh",
        "scripts/identity-center/identity-dashboard-export.sh",
        "docs/identity-center/ENTERPRISE_SSO_IDENTITY_CENTER_GUIDE.md",
        "docs/identity-center/SSO_CONFIGURATION_POLICY.md",
        "docs/identity-center/SCIM_MAPPING_POLICY.md",
        "docs/identity-center/ACCESS_REVIEW_POLICY.md",
        "docs/identity-center/IDENTITY_EVIDENCE_POLICY.md",
        "docs/requirements/NEXT_V47_ENTERPRISE_SSO_IDENTITY_CENTER_REQUIREMENTS.md",
        "assets/identity-center/enterprise_sso_identity_center_features.json",
    ]:
        assert (root / rel).exists(), rel
