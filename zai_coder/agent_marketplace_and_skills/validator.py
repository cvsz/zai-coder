"""Skill manifest validator."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from .models import SkillManifest


def _as_tuple(value: Any) -> tuple[str, ...]:
    if value is None:
        return ()
    if isinstance(value, str):
        return (value,)
    try:
        return tuple(str(item) for item in value)
    except TypeError:
        return (str(value),)


def _extract_hermes_metadata(payload: Mapping[str, Any]) -> dict[str, Any]:
    metadata = payload.get("metadata", {})
    if not isinstance(metadata, Mapping):
        return {}
    hermes = metadata.get("hermes", {})
    if not isinstance(hermes, Mapping):
        return {}
    return dict(hermes)


def validate_skill_manifest_payload(payload: dict) -> dict:
    try:
        hermes_metadata = _extract_hermes_metadata(payload)
        manifest = SkillManifest(
            id=payload.get("id") or payload.get("name", ""),
            name=payload.get("name", ""),
            version=payload.get("version", ""),
            description=payload.get("description", ""),
            category=payload.get("category") or hermes_metadata.get("category", "general"),
            entrypoint=payload.get("entrypoint", "SKILL.md"),
            required_permissions=_as_tuple(payload.get("required_permissions", ["skill:view"])),
            compatible_agent_types=_as_tuple(payload.get("compatible_agent_types", ["builder"])),
            tags=_as_tuple(payload.get("tags") or hermes_metadata.get("tags", [])),
            platforms=_as_tuple(payload.get("platforms", [])),
            source=payload.get("source", "local"),
            source_slug=payload.get("source_slug", ""),
            required_environment_variables=_as_tuple(payload.get("required_environment_variables", [])),
            hermes_metadata=hermes_metadata,
        )
    except Exception as exc:
        return {"ok": False, "issues": [str(exc)]}
    issues = manifest.validate()
    return {"ok": not issues, "issues": issues, "manifest": manifest.to_dict()}


def manifest_security_report(manifest: SkillManifest) -> dict:
    issues = []
    if "providers:apply" in manifest.required_permissions:
        issues.append("skill requests provider apply permission")
    if "execution:apply" in manifest.required_permissions:
        issues.append("skill requests execution apply permission")
    if manifest.category in {"infrastructure", "billing"} and not manifest.required_permissions:
        issues.append("sensitive category should declare required permissions")
    if manifest.source in {"url", "well-known", "github", "skills-sh", "clawhub", "lobehub", "browse-sh"} and not manifest.source_slug:
        issues.append("external or hub skill should keep its source_slug for auditability")
    if manifest.hermes_metadata.get("requires_toolsets") and "skill:view" not in manifest.required_permissions:
        issues.append("toolset-gated skills must remain visible for review")
    return {"ok": not issues, "issues": issues, "manifest": manifest.to_dict()}
