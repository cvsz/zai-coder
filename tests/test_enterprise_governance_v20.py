from pathlib import Path
import tempfile

from zai_coder.enterprise_governance.models import GovernancePolicy, RiskItem, ChangeRequest
from zai_coder.enterprise_governance.policy_engine import policy_manifest, governance_gate, evaluate_operation
from zai_coder.enterprise_governance.role_matrix import role_allows, permissions_for_role, role_matrix_manifest
from zai_coder.enterprise_governance.compliance import compliance_checklist, compliance_summary
from zai_coder.enterprise_governance.evidence import collect_evidence, write_evidence_bundle
from zai_coder.enterprise_governance.change_approval import approval_requirement, change_approval_decision, sample_change_request
from zai_coder.enterprise_governance.risk_register import risk_register, risk_summary
from zai_coder.enterprise_governance.data_retention import data_retention_policy, data_retention_checklist
from zai_coder.enterprise_governance.tenant_isolation import tenant_isolation_policy, tenant_isolation_check
from zai_coder.enterprise_governance.release_gate import release_readiness_gate, sample_release_status
from zai_coder.enterprise_governance.ui.pages import render_governance_overview, render_policies_page, render_roles_page, render_risks_page, render_release_gate_page, render_compliance_page
from zai_coder.enterprise_governance.routes import (
    route_governance_status,
    route_policy_manifest,
    route_governance_gate,
    route_role_matrix,
    route_role_allows,
    route_compliance_checklist,
    route_compliance_summary,
    route_evidence_collect,
    route_evidence_bundle,
    route_change_approval,
    route_risk_register,
    route_data_retention,
    route_tenant_isolation,
    route_release_gate,
    route_governance_page,
    route_policies_page,
    route_roles_page,
    route_risks_page,
    route_release_gate_page,
    route_compliance_page,
)


def test_models_validation():
    assert GovernancePolicy("p", "name", "desc").validate() == []
    assert GovernancePolicy("", "", "desc", severity="bad").validate()
    assert RiskItem("r", "risk", "security", 2, 5, "mitigate").score == 10
    assert RiskItem("", "", "x", 0, 6, "").validate()
    assert ChangeRequest("c", "change", "me", "high", "target").validate() == []


def test_policy_engine():
    assert policy_manifest()
    blocked = governance_gate({"mutating": True, "apply": True, "approval_id": "", "dry_run_completed": False})
    assert blocked["allowed"] is False
    allowed = governance_gate({"mutating": False, "apply": False, "secret_scan_ok": True})
    assert allowed["allowed"] is True
    decisions = evaluate_operation({"public_exposure": True, "cloudflare_access_enabled": False})
    assert any(not d.allowed for d in decisions)


def test_role_matrix():
    assert role_allows("owner", "anything")
    assert role_allows("admin", "governance:approve")
    assert not role_allows("viewer", "execution:apply")
    assert "observability:view" in permissions_for_role("viewer")
    assert "admin" in role_matrix_manifest()


def test_compliance_evidence():
    checklist = compliance_checklist()
    assert checklist
    status = {item["id"]: True for item in checklist}
    assert compliance_summary(status)["ok"] is True
    assert compliance_summary({})["ok"] is False
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        (root / "docs/cloudflare").mkdir(parents=True)
        (root / "docs/cloudflare/CLOUDFLARE_ACCESS_CHECKLIST.md").write_text("ok", encoding="utf-8")
        result = collect_evidence(root)
        assert "items" in result
        out = write_evidence_bundle(root)
        assert Path(out).exists()


def test_change_risk_data_tenant_release():
    assert approval_requirement("high") == 2
    decision = change_approval_decision(sample_change_request())
    assert decision["allowed"] is False
    assert risk_register()
    assert risk_summary()["total"] >= 1
    assert data_retention_policy()["redaction_required"] is True
    assert data_retention_checklist()
    assert tenant_isolation_policy()["required"] is True
    assert tenant_isolation_check({"organization_id":"o","workspace_id":"w","actor":"a"})["ok"] is True
    assert tenant_isolation_check({})["ok"] is False
    assert release_readiness_gate(sample_release_status())["allowed"] is True
    assert release_readiness_gate({})["allowed"] is False


def test_ui_pages():
    assert "Enterprise Governance" in render_governance_overview()
    assert "Policies" in render_policies_page()
    assert "Role Matrix" in render_roles_page()
    assert "Risk Register" in render_risks_page()
    assert "Release Readiness Gate" in render_release_gate_page()
    assert "Compliance Checklist" in render_compliance_page()


def test_routes():
    assert route_governance_status()["ok"] is True
    assert route_policy_manifest()["policies"]
    assert route_governance_gate({"mutating": False})["allowed"] is True
    assert route_role_matrix()["roles"]
    assert route_role_allows("viewer", "governance:view")["allowed"] is True
    assert route_compliance_checklist()["items"]
    assert "items" in route_compliance_summary({})
    assert "items" in route_evidence_collect(".")
    assert "path" in route_evidence_bundle(".")
    assert "allowed" in route_change_approval()
    assert route_risk_register()["risks"]
    assert route_data_retention()["policy"]
    assert route_tenant_isolation({"organization_id":"o","workspace_id":"w","actor":"a"})["check"]["ok"] is True
    assert "allowed" in route_release_gate()
    assert route_governance_page()["content_type"] == "text/html"
    assert route_policies_page()["content_type"] == "text/html"
    assert route_roles_page()["content_type"] == "text/html"
    assert route_risks_page()["content_type"] == "text/html"
    assert route_release_gate_page()["content_type"] == "text/html"
    assert route_compliance_page()["content_type"] == "text/html"


def test_docs_scripts_assets_exist():
    root = Path(__file__).resolve().parents[1]
    for rel in [
        "scripts/governance/governance-status.sh",
        "scripts/governance/policy-manifest.sh",
        "scripts/governance/governance-gate.sh",
        "scripts/governance/role-matrix.sh",
        "scripts/governance/compliance-checklist.sh",
        "scripts/governance/evidence-collect.sh",
        "scripts/governance/change-approval.sh",
        "scripts/governance/risk-register.sh",
        "scripts/governance/data-retention.sh",
        "scripts/governance/tenant-isolation.sh",
        "scripts/governance/release-gate.sh",
        "scripts/governance/dashboard-export.sh",
        "docs/governance/ENTERPRISE_GOVERNANCE_GUIDE.md",
        "docs/governance/POLICY_ENGINE.md",
        "docs/governance/ROLE_PERMISSION_MATRIX.md",
        "docs/governance/COMPLIANCE_AND_EVIDENCE.md",
        "docs/governance/RISK_REGISTER.md",
        "docs/governance/RELEASE_READINESS_GATE.md",
        "docs/requirements/NEXT_V20_ENTERPRISE_GOVERNANCE_REQUIREMENTS.md",
        "assets/governance/enterprise_governance_features.json",
    ]:
        assert (root / rel).exists(), rel
