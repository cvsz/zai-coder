"""Template and Content Studio models.

The content studio is local-first and review-first. It renders local templates
with supplied variables only. It does not publish content externally, send
messages, or call external generation providers.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass(frozen=True)
class ContentTemplate:
    id: str
    title: str
    template_type: str
    body: str
    variables: tuple[str, ...] = ()
    audience: str = "customer"
    channel: str = "document"
    status: str = "draft"
    visibility: str = "private"
    created_at: str = field(default_factory=now_iso)

    def validate(self) -> list[str]:
        issues: list[str] = []
        if not self.id or not self.title or not self.body:
            issues.append("template id, title, and body required")
        if self.template_type not in {"email", "document", "social", "help_article", "release_note", "proposal", "onboarding"}:
            issues.append("invalid template_type")
        if self.audience not in {"customer", "admin", "internal", "public", "investor"}:
            issues.append("invalid audience")
        if self.channel not in {"email", "document", "portal", "social", "markdown", "html"}:
            issues.append("invalid channel")
        if self.status not in {"draft", "review", "approved", "archived"}:
            issues.append("invalid status")
        if self.visibility not in {"private", "customer", "public", "internal"}:
            issues.append("invalid visibility")
        forbidden = {"password", "token", "secret", "api key", "credit card"}
        if any(term in self.body.lower() for term in forbidden):
            issues.append("template may contain sensitive material")
        return issues

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "template_type": self.template_type,
            "body": self.body,
            "variables": list(self.variables),
            "audience": self.audience,
            "channel": self.channel,
            "status": self.status,
            "visibility": self.visibility,
            "created_at": self.created_at,
        }


@dataclass(frozen=True)
class ContentBrief:
    id: str
    title: str
    objective: str
    audience: str
    channel: str
    tone: str = "professional"
    required_points: tuple[str, ...] = ()
    status: str = "draft"
    created_at: str = field(default_factory=now_iso)

    def validate(self) -> list[str]:
        issues: list[str] = []
        if not self.id or not self.title or not self.objective:
            issues.append("brief id, title, and objective required")
        if self.audience not in {"customer", "admin", "internal", "public", "investor"}:
            issues.append("invalid audience")
        if self.channel not in {"email", "document", "portal", "social", "markdown", "html"}:
            issues.append("invalid channel")
        if self.tone not in {"professional", "friendly", "technical", "executive", "supportive", "concise"}:
            issues.append("invalid tone")
        if self.status not in {"draft", "review", "approved", "archived"}:
            issues.append("invalid brief status")
        return issues

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "objective": self.objective,
            "audience": self.audience,
            "channel": self.channel,
            "tone": self.tone,
            "required_points": list(self.required_points),
            "status": self.status,
            "created_at": self.created_at,
        }


@dataclass(frozen=True)
class RenderedContent:
    id: str
    template_id: str
    title: str
    content: str
    channel: str
    variables: dict[str, Any] = field(default_factory=dict)
    dry_run: bool = True
    created_at: str = field(default_factory=now_iso)

    def validate(self) -> list[str]:
        issues: list[str] = []
        if not self.id or not self.template_id or not self.title:
            issues.append("rendered content id, template_id, and title required")
        if not self.dry_run:
            issues.append("rendered content must be dry-run/export-only by default")
        if len(self.content) > 100000:
            issues.append("rendered content too large")
        forbidden = {"password", "token", "secret", "api key", "credit card"}
        if any(term in self.content.lower() for term in forbidden):
            issues.append("rendered content may contain sensitive material")
        return issues

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "template_id": self.template_id,
            "title": self.title,
            "content": self.content,
            "channel": self.channel,
            "variables": dict(self.variables),
            "dry_run": self.dry_run,
            "created_at": self.created_at,
        }


@dataclass(frozen=True)
class ContentApproval:
    id: str
    content_id: str
    status: str = "pending"
    reviewer: str = "owner"
    notes: str = ""
    created_at: str = field(default_factory=now_iso)

    def validate(self) -> list[str]:
        issues: list[str] = []
        if not self.id or not self.content_id:
            issues.append("approval id and content_id required")
        if self.status not in {"pending", "approved", "rejected", "changes_requested"}:
            issues.append("invalid approval status")
        if self.status == "approved" and not self.reviewer:
            issues.append("reviewer required for approval")
        return issues

    def to_dict(self) -> dict:
        return self.__dict__.copy()


@dataclass(frozen=True)
class ContentAuditEvent:
    id: str
    actor: str
    action: str
    target: str
    payload: dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=now_iso)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "actor": self.actor,
            "action": self.action,
            "target": self.target,
            "payload": dict(self.payload),
            "created_at": self.created_at,
        }
