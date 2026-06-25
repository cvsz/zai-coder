"""Privacy and retention guards for usage analytics."""

from __future__ import annotations

FORBIDDEN_METADATA_KEYS = {"email", "password", "token", "secret", "api_key", "credit_card", "phone"}


def redact_metadata(metadata: dict) -> dict:
    redacted = {}
    for key, value in metadata.items():
        if str(key).lower() in FORBIDDEN_METADATA_KEYS:
            redacted[key] = "<redacted>"
        else:
            redacted[key] = value
    return redacted


def privacy_gate(event_payload: dict) -> dict:
    metadata = event_payload.get("metadata", {})
    forbidden = sorted(FORBIDDEN_METADATA_KEYS & {str(key).lower() for key in metadata.keys()})
    return {
        "allowed": not forbidden,
        "blocked": [f"forbidden metadata key: {key}" for key in forbidden],
        "redacted_metadata": redact_metadata(metadata),
    }


def analytics_retention_policy() -> dict:
    return {
        "raw_event_retention_days": 90,
        "aggregate_retention_days": 1095,
        "exports_redact_metadata": True,
        "external_publish": False,
        "no_pii_by_default": True,
    }


def export_safety_gate(report_payload: dict, external_publish_requested: bool = False, approval_id: str = "") -> dict:
    blocked = []
    if external_publish_requested:
        blocked.append("external analytics publishing is disabled")
    if external_publish_requested and not approval_id.startswith("approved_"):
        blocked.append("external publishing would require approval")
    if not report_payload.get("dry_run", True):
        blocked.append("report must remain dry-run/export-only")
    return {"allowed": not blocked, "blocked": blocked, "report_id": report_payload.get("id")}
