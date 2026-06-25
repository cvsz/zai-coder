"""Enterprise Compliance Center route registry."""

from __future__ import annotations

from zai_coder.enterprise_compliance_center.control import compliance_center_status, compliance_overview, evidence_demo, readiness_demo
from zai_coder.enterprise_compliance_center.frameworks import framework_catalog, framework_validation_report
from zai_coder.enterprise_compliance_center.controls import control_library, controls_for_framework, control_validation_report
from zai_coder.enterprise_compliance_center.data_register import processing_register, processing_register_validation, retention_summary
from zai_coder.enterprise_compliance_center.risk_matrix import risk_control_matrix, risk_acceptance_gate
from zai_coder.enterprise_compliance_center.attestations import policy_catalog, create_attestation, attestation_gap_report
from zai_coder.enterprise_compliance_center.legal_hold import legal_hold_policy, retention_delete_gate
from zai_coder.enterprise_compliance_center.readiness import audit_package_plan, audit_readiness_gate
from zai_coder.enterprise_compliance_center.reporting import compliance_report_markdown, write_compliance_report
from zai_coder.enterprise_compliance_center.audit import ComplianceAuditLog
from zai_coder.enterprise_compliance_center.ui.pages import render_compliance_overview_page, render_frameworks_page, render_controls_page, render_risks_page


def route_compliance_status() -> dict:
    return {
        "ok": True,
        "service": "zai-enterprise-compliance-center",
        "systems": [
            "compliance_framework_catalog",
            "control_library",
            "evidence_mapper",
            "audit_readiness_gate",
            "data_processing_register",
            "risk_control_matrix",
            "policy_attestation",
            "retention_legal_hold_guard",
            "compliance_dashboard",
            "compliance_audit_log",
        ],
    }


def route_compliance_overview() -> dict:
    return compliance_overview()


def route_frameworks() -> dict:
    return {"frameworks": framework_catalog(), "validation": framework_validation_report()}


def route_controls(framework_id: str = "soc2") -> dict:
    return {"controls": controls_for_framework(framework_id), "all_controls": control_library(), "validation": control_validation_report()}


def route_evidence_demo() -> dict:
    return evidence_demo(".")


def route_processing_register() -> dict:
    return {"records": processing_register(), "validation": processing_register_validation(), "retention": retention_summary()}


def route_risk_matrix() -> dict:
    rows = risk_control_matrix()
    return {"risks": rows, "acceptance_gate": risk_acceptance_gate(rows[0], "approved_manual_001")}


def route_policy_attestations() -> dict:
    attestations = [
        create_attestation("policy-security", "admin", "attested").to_dict(),
        create_attestation("policy-data-retention", "admin", "pending").to_dict(),
    ]
    return {"policies": policy_catalog(), "attestations": attestations, "gaps": attestation_gap_report(attestations, ["policy-security", "policy-data-retention"])}


def route_legal_hold_policy() -> dict:
    record = processing_register()[0]
    expired_record = dict(record)
    expired_record["retention_days"] = 0
    return {"policy": legal_hold_policy(), "delete_gate": retention_delete_gate(expired_record, legal_hold=False, approval_id="approved_manual_001")}


def route_audit_readiness_demo() -> dict:
    return readiness_demo(".")


def route_audit_package_plan() -> dict:
    return audit_package_plan("soc2")


def route_compliance_report() -> dict:
    return {"markdown": compliance_report_markdown(), "path": write_compliance_report(".")}


def route_compliance_audit() -> dict:
    return {"events": ComplianceAuditLog().list_events()}


def route_compliance_page() -> dict:
    return {"content_type": "text/html", "html": render_compliance_overview_page()}


def route_compliance_frameworks_page() -> dict:
    return {"content_type": "text/html", "html": render_frameworks_page()}


def route_compliance_controls_page() -> dict:
    return {"content_type": "text/html", "html": render_controls_page()}


def route_compliance_risks_page() -> dict:
    return {"content_type": "text/html", "html": render_risks_page()}
