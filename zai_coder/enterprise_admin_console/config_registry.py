"""Admin configuration registry with secret redaction."""

from __future__ import annotations

from .models import ConfigEntry


DEFAULT_CONFIG = [
    ConfigEntry("app.name", "ZAI Coder Control Plane", "app", False, False),
    ConfigEntry("app.mode", "local-first", "app", False, True),
    ConfigEntry("security.auth_required", "true", "security", False, True),
    ConfigEntry("providers.github.token", "<redacted>", "providers", True, False),
    ConfigEntry("billing.mode", "draft-only", "billing", False, True),
    ConfigEntry("updates.channel", "stable", "release", False, True),
]


def config_registry() -> list[dict]:
    return [entry.to_dict() for entry in DEFAULT_CONFIG]


def config_validation_report() -> dict:
    reports = [{"key": entry.key, "issues": entry.validate()} for entry in DEFAULT_CONFIG]
    return {"ok": all(not item["issues"] for item in reports), "reports": reports}


def config_change_plan(key: str, value: str, approval_id: str = "") -> dict:
    match = next((entry for entry in DEFAULT_CONFIG if entry.key == key), None)
    if not match:
        raise ValueError(f"unknown config key: {key}")
    blocked = []
    if match.secret:
        blocked.append("secret values cannot be changed through admin console")
    if not match.mutable:
        blocked.append("config key is immutable")
    if key.startswith("security.") and not approval_id.startswith("approved_"):
        blocked.append("security config changes require approval")
    return {"dry_run": True, "allowed": not blocked, "blocked": blocked, "key": key, "new_value": "<redacted>" if match.secret else value}
