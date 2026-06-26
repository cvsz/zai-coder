"""Agent Marketplace and Skills models.

Marketplace operations are local-first. Skill installation is policy-gated,
tenant-scoped, auditable, and dry-run-first.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


SUPPORTED_SKILL_SOURCES = {
    "local",
    "bundled",
    "official",
    "skills-sh",
    "well-known",
    "github",
    "url",
    "clawhub",
    "lobehub",
    "browse-sh",
}

SUPPORTED_PLATFORMS = {"linux", "macos", "windows"}


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _safe_slug(value: str) -> bool:
    return bool(value) and "/" not in value and "\\" not in value and ".." not in value


@dataclass(frozen=True)
class SkillManifest:
    id: str
    name: str
    version: str
    description: str
    category: str = "general"
    entrypoint: str = "SKILL.md"
    required_permissions: tuple[str, ...] = ("skill:view",)
    compatible_agent_types: tuple[str, ...] = ("builder", "operator")
    tags: tuple[str, ...] = ()
    platforms: tuple[str, ...] = ()
    source: str = "local"
    source_slug: str = ""
    required_environment_variables: tuple[str, ...] = ()
    hermes_metadata: dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=now_iso)

    def validate(self) -> list[str]:
        issues: list[str] = []
        if not self.id or not self.name or not self.version:
            issues.append("skill id, name, and version required")
        if not _safe_slug(self.id):
            issues.append("unsafe skill id")
        if len(self.description.strip()) > 120:
            issues.append("description should stay concise for progressive disclosure")
        if not self.entrypoint.endswith(".md"):
            issues.append("entrypoint must be markdown")
        if self.entrypoint.startswith("/") or ".." in self.entrypoint:
            issues.append("unsafe entrypoint path")
        if any("/" in p or "\\" in p or ".." in p for p in self.required_permissions):
            issues.append("unsafe permission value")
        if any(platform not in SUPPORTED_PLATFORMS for platform in self.platforms):
            issues.append("unsupported platform")
        if self.source not in SUPPORTED_SKILL_SOURCES:
            issues.append("unsupported skill source")
        if self.source != "local" and not self.source_slug:
            issues.append("hub or external skill sources require source_slug")
        if any("/" in name or "\\" in name or ".." in name for name in self.required_environment_variables):
            issues.append("unsafe environment variable name")
        return issues

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "version": self.version,
            "description": self.description,
            "category": self.category,
            "entrypoint": self.entrypoint,
            "required_permissions": list(self.required_permissions),
            "compatible_agent_types": list(self.compatible_agent_types),
            "tags": list(self.tags),
            "platforms": list(self.platforms),
            "source": self.source,
            "source_slug": self.source_slug,
            "required_environment_variables": list(self.required_environment_variables),
            "hermes_metadata": dict(self.hermes_metadata),
            "created_at": self.created_at,
        }


@dataclass(frozen=True)
class AgentListing:
    id: str
    name: str
    agent_type: str
    description: str
    default_skills: tuple[str, ...] = ()
    tags: tuple[str, ...] = ()
    status: str = "available"
    created_at: str = field(default_factory=now_iso)

    def validate(self) -> list[str]:
        issues: list[str] = []
        if not self.id or not self.name or not self.agent_type:
            issues.append("agent listing id, name, and agent_type required")
        if self.status not in {"available", "deprecated", "hidden"}:
            issues.append("invalid listing status")
        if not _safe_slug(self.id):
            issues.append("unsafe agent listing id")
        return issues

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "agent_type": self.agent_type,
            "description": self.description,
            "default_skills": list(self.default_skills),
            "tags": list(self.tags),
            "status": self.status,
            "created_at": self.created_at,
        }


@dataclass(frozen=True)
class SkillInstallation:
    id: str
    skill_id: str
    org_id: str
    workspace_id: str
    enabled: bool = False
    installed_by: str = "system"
    installed_at: str = field(default_factory=now_iso)

    def validate(self) -> list[str]:
        issues = []
        if not self.id or not self.skill_id:
            issues.append("installation id and skill_id required")
        if not self.org_id or not self.workspace_id:
            issues.append("installation requires tenant context")
        return issues

    def to_dict(self) -> dict:
        return self.__dict__.copy()


@dataclass(frozen=True)
class MarketplaceAuditEvent:
    id: str
    org_id: str
    workspace_id: str
    actor: str
    action: str
    target: str
    payload: dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=now_iso)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "org_id": self.org_id,
            "workspace_id": self.workspace_id,
            "actor": self.actor,
            "action": self.action,
            "target": self.target,
            "payload": dict(self.payload),
            "created_at": self.created_at,
        }


@dataclass(frozen=True)
class SkillReview:
    id: str
    skill_id: str
    reviewer: str
    rating: int
    comment: str
    created_at: str = field(default_factory=now_iso)

    def validate(self) -> list[str]:
        issues = []
        if not self.id or not self.skill_id or not self.reviewer:
            issues.append("review id, skill_id, and reviewer required")
        if not (1 <= self.rating <= 5):
            issues.append("rating must be 1..5")
        if len(self.comment) > 2000:
            issues.append("comment too large")
        return issues

    def to_dict(self) -> dict:
        return self.__dict__.copy()
