"""Compliance control library."""

from __future__ import annotations

from .models import ComplianceControl


DEFAULT_CONTROLS = [
    ComplianceControl(
        "cc-access-001", "soc2", "security", "Access control policy",
        "Role-based access and tenant isolation controls are defined and reviewed.",
        status="implemented",
        evidence_required=("role_matrix", "tenant_isolation_policy", "access_review_log"),
    ),
    ComplianceControl(
        "cc-audit-001", "soc2", "security", "Audit logging",
        "Security-relevant actions are logged and retained.",
        status="implemented",
        evidence_required=("audit_log_sample", "retention_policy"),
    ),
    ComplianceControl(
        "iso-ops-001", "iso27001", "operations", "Operational monitoring",
        "Operational metrics, alerts, incident response, and postmortems are maintained.",
        status="implemented",
        evidence_required=("observability_dashboard", "incident_report", "postmortem"),
    ),
    ComplianceControl(
        "gdpr-data-001", "gdpr", "data_processing", "Processing register",
        "Data processing purposes, lawful basis, categories, and retention are documented.",
        status="planned",
        evidence_required=("processing_register", "retention_policy"),
    ),
    ComplianceControl(
        "pdpa-consent-001", "pdpa-th", "consent", "Consent and lawful basis register",
        "Personal data usage basis and consent process are documented.",
        status="planned",
        evidence_required=("lawful_basis_register", "privacy_notice"),
    ),
]


def control_library() -> list[dict]:
    return [control.to_dict() for control in DEFAULT_CONTROLS]


def controls_for_framework(framework_id: str) -> list[dict]:
    return [control.to_dict() for control in DEFAULT_CONTROLS if control.framework_id == framework_id]


def find_control(control_id: str) -> ComplianceControl:
    for control in DEFAULT_CONTROLS:
        if control.id == control_id:
            return control
    raise ValueError(f"unknown control: {control_id}")


def control_validation_report() -> dict:
    reports = [{"id": control.id, "issues": control.validate()} for control in DEFAULT_CONTROLS]
    return {"ok": all(not item["issues"] for item in reports), "reports": reports}
