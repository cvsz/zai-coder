"""Skill manifest validator."""

from __future__ import annotations

from .models import SkillManifest


def validate_skill_manifest_payload(payload: dict) -> dict:
    try:
        manifest = SkillManifest(
            id=payload.get("id", ""),
            name=payload.get("name", ""),
            version=payload.get("version", ""),
            description=payload.get("description", ""),
            category=payload.get("category", "general"),
            entrypoint=payload.get("entrypoint", "SKILL.md"),
            required_permissions=tuple(payload.get("required_permissions", ["skill:view"])),
            compatible_agent_types=tuple(payload.get("compatible_agent_types", ["builder"])),
            tags=tuple(payload.get("tags", [])),
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
    return {"ok": not issues, "issues": issues, "manifest": manifest.to_dict()}
