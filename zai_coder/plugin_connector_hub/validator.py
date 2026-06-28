"""Connector manifest validator and security checks."""

from __future__ import annotations

from zai_coder.core.booleans import coerce_bool
from .models import ConnectorManifest


def validate_connector_manifest_payload(payload: dict) -> dict:
    try:
        manifest = ConnectorManifest(
            id=payload.get("id", ""),
            name=payload.get("name", ""),
            provider=payload.get("provider", ""),
            version=payload.get("version", ""),
            description=payload.get("description", ""),
            category=payload.get("category", "general"),
            required_env=tuple(payload.get("required_env", [])),
            required_permissions=tuple(payload.get("required_permissions", ["connector:view"])),
            supported_actions=tuple(payload.get("supported_actions", ["status"])),
            webhook_supported=coerce_bool(payload.get("webhook_supported", False)),
            sync_supported=coerce_bool(payload.get("sync_supported", True)),
        )
    except Exception as exc:
        return {"ok": False, "issues": [str(exc)]}
    issues = manifest.validate()
    return {"ok": not issues, "issues": issues, "manifest": manifest.to_dict()}


def connector_security_report(manifest: ConnectorManifest) -> dict:
    issues = []
    sensitive_permissions = {"providers:apply", "execution:apply", "billing:write"}
    requested = set(manifest.required_permissions)
    if requested & sensitive_permissions:
        issues.append("connector requests sensitive apply/write permission")
    if manifest.webhook_supported and not any(env.endswith("_WEBHOOK_SECRET") for env in manifest.required_env):
        issues.append("webhook connector should declare webhook secret env")
    if manifest.category == "infrastructure" and "providers:plan" not in requested:
        issues.append("infrastructure connector should request providers:plan")
    return {"ok": not issues, "issues": issues, "manifest": manifest.to_dict()}
