"""Notification and Communication Center models.

The notification center is local-first and draft-only by default. It creates
reviewable message drafts and delivery plans, but does not send email, SMS,
Slack, webhook, or other external communication automatically.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass(frozen=True)
class NotificationTemplate:
    id: str
    title: str
    channel: str
    subject: str
    body: str
    variables: tuple[str, ...] = ()
    audience: str = "customer"
    status: str = "draft"
    visibility: str = "private"
    created_at: str = field(default_factory=now_iso)

    def validate(self) -> list[str]:
        issues: list[str] = []
        if not self.id or not self.title or not self.body:
            issues.append("template id, title, and body required")
        if self.channel not in {"portal", "email", "sms", "slack", "webhook", "in_app"}:
            issues.append("invalid channel")
        if self.audience not in {"customer", "admin", "internal", "support", "public"}:
            issues.append("invalid audience")
        if self.status not in {"draft", "review", "approved", "archived"}:
            issues.append("invalid status")
        if self.visibility not in {"private", "customer", "public", "internal"}:
            issues.append("invalid visibility")
        forbidden = {"password", "token", "secret", "api key", "credit card"}
        text = f"{self.subject} {self.body}".lower()
        if any(term in text for term in forbidden):
            issues.append("template may contain sensitive material")
        return issues

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "channel": self.channel,
            "subject": self.subject,
            "body": self.body,
            "variables": list(self.variables),
            "audience": self.audience,
            "status": self.status,
            "visibility": self.visibility,
            "created_at": self.created_at,
        }


@dataclass(frozen=True)
class NotificationPreference:
    id: str
    customer_id: str
    channel: str
    enabled: bool = True
    topic: str = "product"
    frequency: str = "immediate"

    def validate(self) -> list[str]:
        issues: list[str] = []
        if not self.id or not self.customer_id:
            issues.append("preference id and customer_id required")
        if self.channel not in {"portal", "email", "sms", "slack", "webhook", "in_app"}:
            issues.append("invalid channel")
        if self.topic not in {"product", "billing", "support", "security", "roadmap", "release", "system"}:
            issues.append("invalid topic")
        if self.frequency not in {"immediate", "daily", "weekly", "never"}:
            issues.append("invalid frequency")
        return issues

    def to_dict(self) -> dict:
        return self.__dict__.copy()


@dataclass(frozen=True)
class NotificationDraft:
    id: str
    template_id: str
    channel: str
    subject: str
    body: str
    recipient_ref: str
    topic: str = "product"
    status: str = "draft"
    dry_run: bool = True
    created_at: str = field(default_factory=now_iso)

    def validate(self) -> list[str]:
        issues: list[str] = []
        if not self.id or not self.template_id or not self.recipient_ref:
            issues.append("draft id, template_id, and recipient_ref required")
        if self.channel not in {"portal", "email", "sms", "slack", "webhook", "in_app"}:
            issues.append("invalid channel")
        if self.status not in {"draft", "review", "approved", "queued", "cancelled"}:
            issues.append("invalid draft status")
        if not self.dry_run:
            issues.append("notification drafts must be dry-run by default")
        forbidden = {"password", "token", "secret", "api key", "credit card"}
        if any(term in f"{self.subject} {self.body}".lower() for term in forbidden):
            issues.append("draft may contain sensitive material")
        return issues

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "template_id": self.template_id,
            "channel": self.channel,
            "subject": self.subject,
            "body": self.body,
            "recipient_ref": self.recipient_ref,
            "topic": self.topic,
            "status": self.status,
            "dry_run": self.dry_run,
            "created_at": self.created_at,
        }


@dataclass(frozen=True)
class CommunicationThread:
    id: str
    customer_id: str
    subject: str
    messages: tuple[dict[str, Any], ...] = ()
    status: str = "open"
    created_at: str = field(default_factory=now_iso)

    def validate(self) -> list[str]:
        issues: list[str] = []
        if not self.id or not self.customer_id or not self.subject:
            issues.append("thread id, customer_id, and subject required")
        if self.status not in {"open", "pending", "resolved", "closed"}:
            issues.append("invalid thread status")
        return issues

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "customer_id": self.customer_id,
            "subject": self.subject,
            "messages": [dict(message) for message in self.messages],
            "status": self.status,
            "created_at": self.created_at,
        }


@dataclass(frozen=True)
class NotificationAuditEvent:
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
