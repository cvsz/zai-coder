"""Data processing register."""

from __future__ import annotations

from .models import DataProcessingRecord


DEFAULT_PROCESSING_RECORDS = [
    DataProcessingRecord("dpr-audit", "audit-log", "operational_metadata", "security auditability", 365, "legitimate_interest", "global", False),
    DataProcessingRecord("dpr-billing", "billing", "billing_metadata", "subscription and usage accounting", 2555, "contract", "global", False),
    DataProcessingRecord("dpr-user-profile", "user-profile", "contact_data", "account administration", 1095, "contract", "global", True),
]


def processing_register() -> list[dict]:
    return [record.to_dict() for record in DEFAULT_PROCESSING_RECORDS]


def processing_register_validation() -> dict:
    reports = [{"id": record.id, "issues": record.validate()} for record in DEFAULT_PROCESSING_RECORDS]
    return {"ok": all(not item["issues"] for item in reports), "reports": reports}


def retention_summary() -> dict:
    records = processing_register()
    return {
        "max_retention_days": max(r["retention_days"] for r in records),
        "pii_records": [r for r in records if r["pii"]],
        "records": records,
    }
