from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

@dataclass(frozen=True)
class ApiEndpoint:
    id: str
    method: str
    path: str
    summary: str
    tag: str = "core"
    auth_required: bool = True
    stability: str = "stable"
    def validate(self) -> list[str]:
        issues=[]
        if not self.id or not self.method or not self.path or not self.summary: issues.append("endpoint id, method, path, and summary required")
        if self.method not in {"GET","POST","PUT","PATCH","DELETE"}: issues.append("invalid method")
        if not self.path.startswith("/"): issues.append("path must start with /")
        if self.stability not in {"experimental","beta","stable","deprecated"}: issues.append("invalid stability")
        return issues
    def to_dict(self): return self.__dict__.copy()

@dataclass(frozen=True)
class SdkSnippet:
    id: str
    language: str
    title: str
    code: str
    endpoint_id: str
    safety_note: str = "Example only. Use non-production credentials."
    def validate(self) -> list[str]:
        issues=[]
        if not self.id or not self.language or not self.title or not self.code or not self.endpoint_id: issues.append("snippet fields required")
        if self.language not in {"bash","python","javascript","typescript"}: issues.append("invalid language")
        forbidden = {"sk-", "secret", "password", "token_live", "private key"}
        if any(term in self.code.lower() for term in forbidden): issues.append("snippet may contain secret-like content")
        return issues
    def to_dict(self): return self.__dict__.copy()

@dataclass(frozen=True)
class Quickstart:
    id: str
    title: str
    audience: str
    steps: tuple[str, ...]
    status: str = "draft"
    def validate(self) -> list[str]:
        issues=[]
        if not self.id or not self.title or not self.steps: issues.append("quickstart id, title, and steps required")
        if self.audience not in {"developer","admin","operator","customer"}: issues.append("invalid audience")
        if self.status not in {"draft","review","published","archived"}: issues.append("invalid status")
        return issues
    def to_dict(self):
        return {"id": self.id, "title": self.title, "audience": self.audience, "steps": list(self.steps), "status": self.status}

@dataclass(frozen=True)
class DevAuditEvent:
    id: str
    actor: str
    action: str
    target: str
    payload: dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=now_iso)
    def to_dict(self):
        return {"id": self.id, "actor": self.actor, "action": self.action, "target": self.target, "payload": dict(self.payload), "created_at": self.created_at}
