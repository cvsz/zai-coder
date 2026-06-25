"""Compliance center control helpers."""

from __future__ import annotations

from .frameworks import framework_catalog, framework_validation_report
from .controls import control_library, control_validation_report
from .evidence import map_evidence, write_evidence_inventory
from .attestations import create_attestation
from .readiness import audit_readiness_gate, audit_package_plan
from .reporting import write_compliance_report
from .audit import ComplianceAuditLog


def compliance_center_status() -> dict:
    return {
        "ok": True,
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


def evidence_demo(root: str = ".") -> dict:
    evidence_items = [
        map_evidence("cc-access-001", "role_matrix", "docs/infra/cloudflare-risk-register.md").to_dict(),
        map_evidence("cc-access-001", "tenant_isolation_policy", "docs/billing/BILLING_USAGE_ENFORCEMENT_GUIDE.md").to_dict(),
        map_evidence("cc-access-001", "access_review_log", "BUILD_REPORT_V30_SELF_HEALING_OPERATIONS.txt", "report").to_dict(),
    ]
    path = write_evidence_inventory(evidence_items, root)
    return {"evidence": evidence_items, "path": path}


def readiness_demo(root: str = ".") -> dict:
    evidence = evidence_demo(root)["evidence"]
    attestations = [
        create_attestation("policy-security", "admin", "attested").to_dict(),
        create_attestation("policy-data-retention", "admin", "attested").to_dict(),
        create_attestation("policy-incident-response", "operator", "attested").to_dict(),
    ]
    readiness = audit_readiness_gate(evidence, attestations, "approved_manual_001")
    report_path = write_compliance_report(root)
    audit = ComplianceAuditLog().record("system", "compliance.readiness_checked", "audit-readiness", readiness)
    return {"readiness": readiness, "report_path": report_path, "audit": audit.to_dict()}


def compliance_overview() -> dict:
    return {
        "status": compliance_center_status(),
        "frameworks": framework_catalog(),
        "framework_validation": framework_validation_report(),
        "controls": control_library(),
        "control_validation": control_validation_report(),
        "package_plan": audit_package_plan("soc2"),
    }
