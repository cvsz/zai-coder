"""Compliance framework catalog."""

from __future__ import annotations

from .models import ComplianceFramework


DEFAULT_FRAMEWORKS = [
    ComplianceFramework(
        "soc2",
        "SOC 2 Trust Services Criteria",
        "2024",
        "US/global",
        "Security, availability, confidentiality, processing integrity, and privacy criteria.",
        ("security", "availability", "confidentiality", "privacy"),
    ),
    ComplianceFramework(
        "iso27001",
        "ISO/IEC 27001",
        "2022",
        "global",
        "Information security management system controls.",
        ("security_policy", "asset_management", "access_control", "operations", "supplier"),
    ),
    ComplianceFramework(
        "gdpr",
        "GDPR",
        "2018",
        "EU",
        "EU data protection and privacy regulation.",
        ("data_processing", "data_subject_rights", "retention", "security", "breach_response"),
    ),
    ComplianceFramework(
        "pdpa-th",
        "Thailand PDPA",
        "2019",
        "Thailand",
        "Thailand Personal Data Protection Act planning controls.",
        ("data_processing", "consent", "retention", "security", "breach_response"),
    ),
]


def framework_catalog() -> list[dict]:
    return [framework.to_dict() for framework in DEFAULT_FRAMEWORKS]


def find_framework(framework_id: str) -> ComplianceFramework:
    for framework in DEFAULT_FRAMEWORKS:
        if framework.id == framework_id:
            return framework
    raise ValueError(f"unknown framework: {framework_id}")


def framework_validation_report() -> dict:
    reports = [{"id": framework.id, "issues": framework.validate()} for framework in DEFAULT_FRAMEWORKS]
    return {"ok": all(not item["issues"] for item in reports), "reports": reports}
