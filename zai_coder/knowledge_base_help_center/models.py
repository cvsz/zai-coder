"""Knowledge Base and Help Center models.

The help center is local-first and export/review-first. It does not publish
articles externally, send emails, or expose private operational notes in
customer-facing views.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass(frozen=True)
class HelpArticle:
    id: str
    title: str
    body: str
    category: str = "general"
    audience: str = "customer"
    status: str = "draft"
    tags: tuple[str, ...] = ()
    visibility: str = "private"
    created_at: str = field(default_factory=now_iso)

    def validate(self) -> list[str]:
        issues: list[str] = []
        if not self.id or not self.title or not self.body:
            issues.append("article id, title, and body required")
        if self.category not in {"general", "onboarding", "billing", "support", "integrations", "security", "admin", "roadmap"}:
            issues.append("invalid category")
        if self.audience not in {"customer", "admin", "support", "internal"}:
            issues.append("invalid audience")
        if self.status not in {"draft", "review", "published", "archived"}:
            issues.append("invalid status")
        if self.visibility not in {"private", "customer", "public", "internal"}:
            issues.append("invalid visibility")
        forbidden = {"password", "token", "secret", "api key", "credit card"}
        text = f"{self.title} {self.body}".lower()
        if any(term in text for term in forbidden):
            issues.append("article may contain sensitive material")
        return issues

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "body": self.body,
            "category": self.category,
            "audience": self.audience,
            "status": self.status,
            "tags": list(self.tags),
            "visibility": self.visibility,
            "created_at": self.created_at,
        }


@dataclass(frozen=True)
class FAQItem:
    id: str
    question: str
    answer: str
    category: str = "general"
    visibility: str = "customer"
    article_id: str = ""

    def validate(self) -> list[str]:
        issues: list[str] = []
        if not self.id or not self.question or not self.answer:
            issues.append("faq id, question, and answer required")
        if self.visibility not in {"private", "customer", "public", "internal"}:
            issues.append("invalid visibility")
        if "?" not in self.question:
            issues.append("FAQ question should include a question mark")
        return issues

    def to_dict(self) -> dict:
        return self.__dict__.copy()


@dataclass(frozen=True)
class SearchResult:
    id: str
    title: str
    score: float
    kind: str = "article"
    snippet: str = ""
    visibility: str = "customer"

    def validate(self) -> list[str]:
        issues: list[str] = []
        if not self.id or not self.title:
            issues.append("search result id and title required")
        if self.score < 0:
            issues.append("score must be >= 0")
        if self.kind not in {"article", "faq", "guide"}:
            issues.append("invalid result kind")
        return issues

    def to_dict(self) -> dict:
        return self.__dict__.copy()


@dataclass(frozen=True)
class HelpFeedback:
    id: str
    article_id: str
    helpful: bool
    comment: str = ""
    customer_id: str = "anonymous"
    created_at: str = field(default_factory=now_iso)

    def validate(self) -> list[str]:
        issues: list[str] = []
        if not self.id or not self.article_id:
            issues.append("feedback id and article_id required")
        forbidden = {"password", "token", "secret", "api key", "credit card"}
        if any(term in self.comment.lower() for term in forbidden):
            issues.append("feedback comment may contain sensitive material")
        return issues

    def to_dict(self) -> dict:
        return self.__dict__.copy()


@dataclass(frozen=True)
class HelpAuditEvent:
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
