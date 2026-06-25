"""Data retention policy."""

from __future__ import annotations


def data_retention_policy() -> dict:
    return {
        "audit_events_days": 365,
        "execution_journal_days": 180,
        "logs_hot_days": 7,
        "logs_archive_days": 30,
        "backups_days": 14,
        "incident_reports_days": 730,
        "redaction_required": True,
        "excluded_paths": [".git/", "node_modules/", "apps/zlms/", ".env", "credentials.json"],
    }


def data_retention_checklist() -> list[dict]:
    policy = data_retention_policy()
    return [
        {"item": "Audit event retention configured", "value": policy["audit_events_days"], "required": True},
        {"item": "Execution journal retention configured", "value": policy["execution_journal_days"], "required": True},
        {"item": "Log retention configured", "value": policy["logs_archive_days"], "required": True},
        {"item": "Secret redaction required", "value": policy["redaction_required"], "required": True},
    ]
