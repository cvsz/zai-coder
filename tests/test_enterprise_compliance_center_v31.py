from pathlib import Path
import tempfile

from zai_coder.enterprise_compliance_center.models import ComplianceFramework, ComplianceControl, EvidenceItem, DataProcessingRecord, PolicyAttestation
from zai_coder.enterprise_compliance_center.frameworks import framework_catalog, find_framework, framework_validation_report
from zai_coder.enterprise_compliance_center.controls import control_library, controls_for_framework, find_control, control_validation_report
from zai_coder.enterprise_compliance_center.evidence import evidence_path_allowed, map_evidence, evidence_gap_report, write_evidence_inventory
from zai_coder.enterprise_compliance_center.data_register import processing_register, processing_register_validation, retention_summary
from zai_coder.enterprise_compliance_center.risk_matrix import risk_score, risk_level, risk_control_matrix, risk_acceptance_gate
from zai_coder.enterprise_compliance_center.attestations import policy_catalog, create_attestation, attestation_gap_report
from zai_coder.enterprise_compliance_center.legal_hold import retention_delete_gate, legal_hold_policy
from zai_coder.enterprise_compliance_center.readiness import audit_readiness_gate, audit_package_plan
from zai_coder.enterprise_compliance_center.reporting import compliance_report_markdown, write_compliance_report
from zai_coder.enterprise_compliance_center.audit import ComplianceAuditLog
from zai_coder.enterprise_compliance_center.control import compliance_center_status, evidence_demo, readiness_demo, compliance_overview
from zai_coder.enterprise_compliance_center.ui.pages import render_compliance_overview_page, render_frameworks_page, render_controls_page, render_risks_page
from zai_coder.enterprise_compliance_center.routes import (
    route_compliance_status,
    route_compliance_overview,
    route_frameworks,
    route_controls,
    route_evidence_demo,
    route_processing_register,
    route_risk_matrix,
    route_policy_attestations,
    route_legal_hold_policy,
    route_audit_readiness_demo,
    route_audit_package_plan,
    route_compliance_report,
    route_compliance_audit,
    route_compliance_page,
    route_compliance_frameworks_page,
    route_compliance_controls_page,
    route_compliance_risks_page,
)


def test_models_validation():
    assert ComplianceFramework("f", "Framework", "1", control_domains=("security",)).validate() == []
    assert ComplianceFramework("../bad", "", "", control_domains=()).validate()
    assert ComplianceControl("c", "f", "domain", "Title", "Desc", evidence_required=("e",)).validate() == []
    assert ComplianceControl("", "", "", "", "", status="bad").validate()
    assert EvidenceItem("e", "c", "Evidence", "docs/file.md").validate() == []
    assert EvidenceItem("", "", "", ".env", contains_secret=True).validate()
    assert DataProcessingRecord("d", "sys", "cat", "purpose", 30, pii=True).validate() == []
    assert DataProcessingRecord("", "", "", "", -1).validate()
    assert PolicyAttestation("a", "p", "actor", "attested").validate() == []


def test_frameworks_controls_evidence(tmp_path):
    assert framework_catalog()
    assert find_framework("soc2").id == "soc2"
    assert framework_validation_report()["ok"] is True
    assert control_library()
    assert controls_for_framework("soc2")
    assert find_control("cc-access-001").framework_id == "soc2"
    assert control_validation_report()["ok"] is True
    assert evidence_path_allowed("docs/a.md") is True
    assert evidence_path_allowed(".env") is False
    item = map_evidence("cc-access-001", "role_matrix", "docs/roles.md")
    assert item.control_id == "cc-access-001"
    report = evidence_gap_report([find_control("cc-access-001").to_dict()], [item.to_dict()])
    assert report["ok"] is False
    path = write_evidence_inventory([item.to_dict()], tmp_path)
    assert Path(path).exists()


def test_data_risk_attestations_legal_hold():
    assert processing_register()
    assert processing_register_validation()["ok"] is True
    assert retention_summary()["pii_records"]
    assert risk_score(2, 5) == 10
    assert risk_level(20) == "critical"
    rows = risk_control_matrix()
    assert rows[0]["controls"]
    assert risk_acceptance_gate(rows[0], "approved_manual_001")["allowed"] is True
    assert policy_catalog()
    att = create_attestation("policy-security", "admin", "attested")
    gaps = attestation_gap_report([att.to_dict()], ["policy-security", "policy-data-retention"])
    assert gaps["ok"] is False
    record = {"pii": True, "retention_days": 0}
    assert retention_delete_gate(record, False, "")["allowed"] is False
    assert retention_delete_gate(record, False, "approved_manual_001")["allowed"] is True
    assert legal_hold_policy()["legal_hold_blocks_delete"] is True


def test_readiness_reporting_audit(tmp_path):
    evidence = [
        map_evidence("cc-access-001", "role_matrix", "docs/roles.md").to_dict(),
        map_evidence("cc-access-001", "tenant_isolation_policy", "docs/tenant.md").to_dict(),
        map_evidence("cc-access-001", "access_review_log", "BUILD_REPORT.txt", "report").to_dict(),
    ]
    attestations = [
        create_attestation("policy-security", "admin", "attested").to_dict(),
        create_attestation("policy-data-retention", "admin", "attested").to_dict(),
        create_attestation("policy-incident-response", "operator", "attested").to_dict(),
    ]
    readiness = audit_readiness_gate(evidence, attestations, "approved_manual_001")
    assert readiness["allowed"] is False  # other controls still need evidence
    assert audit_package_plan("soc2")["dry_run"] is True
    assert "Enterprise Compliance Center Report" in compliance_report_markdown()
    path = write_compliance_report(tmp_path)
    assert Path(path).exists()
    audit = ComplianceAuditLog(tmp_path / "compliance.db")
    event = audit.record("tester", "compliance.test", "target")
    assert audit.list_events()[0]["id"] == event.id


def test_control_ui_routes(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    assert compliance_center_status()["ok"] is True
    demo = evidence_demo(str(tmp_path))
    assert Path(demo["path"]).exists()
    ready = readiness_demo(str(tmp_path))
    assert Path(ready["report_path"]).exists()
    assert compliance_overview()["status"]["ok"] is True
    assert "Enterprise Compliance Center" in render_compliance_overview_page()
    assert "Frameworks" in render_frameworks_page()
    assert "Controls" in render_controls_page()
    assert "Risks" in render_risks_page()
    assert route_compliance_status()["ok"] is True
    assert route_compliance_overview()["status"]["ok"] is True
    assert route_frameworks()["validation"]["ok"] is True
    assert route_controls("soc2")["controls"]
    assert Path(route_evidence_demo()["path"]).exists()
    assert route_processing_register()["validation"]["ok"] is True
    assert route_risk_matrix()["risks"]
    assert route_policy_attestations()["policies"]
    assert route_legal_hold_policy()["delete_gate"]["allowed"] is True
    assert Path(route_audit_readiness_demo()["report_path"]).exists()
    assert route_audit_package_plan()["dry_run"] is True
    assert Path(route_compliance_report()["path"]).exists()
    assert "events" in route_compliance_audit()
    assert route_compliance_page()["content_type"] == "text/html"
    assert route_compliance_frameworks_page()["content_type"] == "text/html"
    assert route_compliance_controls_page()["content_type"] == "text/html"
    assert route_compliance_risks_page()["content_type"] == "text/html"


def test_docs_scripts_assets_exist():
    root = Path(__file__).resolve().parents[1]
    for rel in [
        "scripts/compliance-center/compliance-status.sh",
        "scripts/compliance-center/frameworks.sh",
        "scripts/compliance-center/controls.sh",
        "scripts/compliance-center/evidence-demo.sh",
        "scripts/compliance-center/processing-register.sh",
        "scripts/compliance-center/risk-matrix.sh",
        "scripts/compliance-center/policy-attestations.sh",
        "scripts/compliance-center/legal-hold-policy.sh",
        "scripts/compliance-center/audit-readiness.sh",
        "scripts/compliance-center/compliance-report.sh",
        "scripts/compliance-center/compliance-audit.sh",
        "scripts/compliance-center/compliance-dashboard-export.sh",
        "docs/compliance-center/ENTERPRISE_COMPLIANCE_CENTER_GUIDE.md",
        "docs/compliance-center/COMPLIANCE_FRAMEWORKS.md",
        "docs/compliance-center/CONTROL_LIBRARY.md",
        "docs/compliance-center/EVIDENCE_MANAGEMENT.md",
        "docs/compliance-center/DATA_PROCESSING_REGISTER.md",
        "docs/compliance-center/RISK_CONTROL_MATRIX.md",
        "docs/requirements/NEXT_V31_ENTERPRISE_COMPLIANCE_CENTER_REQUIREMENTS.md",
        "assets/compliance-center/enterprise_compliance_center_features.json",
    ]:
        assert (root / rel).exists(), rel
