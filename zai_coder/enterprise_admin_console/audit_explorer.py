"""Admin audit explorer."""

from __future__ import annotations

from zai_coder.enterprise_admin_console.models import AdminAuditEvent
from zai_coder.enterprise_compliance_center.audit import ComplianceAuditLog
from zai_coder.enterprise_reporting_board_pack.audit import ReportingAuditLog
from zai_coder.self_healing_operations.audit import HealingAuditLog


def audit_sources() -> list[dict]:
    return [
        {"id": "admin", "name": "Admin Console", "redacted": True},
        {"id": "compliance", "name": "Compliance Center", "redacted": True},
        {"id": "reporting", "name": "Board Pack Reporting", "redacted": True},
        {"id": "healing", "name": "Self-Healing Operations", "redacted": True},
    ]


def audit_query_plan(source: str = "admin", limit: int = 50) -> dict:
    if source not in {item["id"] for item in audit_sources()}:
        raise ValueError(f"unknown audit source: {source}")
    return {
        "dry_run": True,
        "source": source,
        "limit": min(max(limit, 1), 500),
        "redaction": "secrets and tokens redacted",
        "steps": ["validate source", "apply tenant filter", "redact sensitive payload", "return audit rows"],
    }


def unified_audit_preview() -> dict:
    return {
        "sources": audit_sources(),
        "plans": [audit_query_plan(source["id"], 10) for source in audit_sources()],
    }
