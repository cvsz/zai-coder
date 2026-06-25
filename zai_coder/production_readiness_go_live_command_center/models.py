from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

@dataclass(frozen=True)
class ReadinessGate:
    id: str
    title: str
    category: str
    required: bool = True
    status: str = "pending"
    evidence_ref: str = ""
    def validate(self) -> list[str]:
        issues=[]
        if not self.id or not self.title or not self.category: issues.append("gate id, title, and category required")
        if self.category not in {"qa","security","identity","scalability","docs","release","rollback","approval"}: issues.append("invalid category")
        if self.status not in {"pending","passed","failed","waived","blocked"}: issues.append("invalid gate status")
        return issues
    def to_dict(self): return self.__dict__.copy()

@dataclass(frozen=True)
class GoLiveChecklistItem:
    id: str
    title: str
    owner: str
    phase: str = "preflight"
    done: bool = False
    manual_approval: bool = True
    def validate(self) -> list[str]:
        issues=[]
        if not self.id or not self.title or not self.owner: issues.append("checklist id, title, and owner required")
        if self.phase not in {"preflight","launch","monitoring","rollback","post_launch"}: issues.append("invalid phase")
        if not self.manual_approval: issues.append("go-live checklist items require manual approval by default")
        return issues
    def to_dict(self): return self.__dict__.copy()

@dataclass(frozen=True)
class LaunchAction:
    id: str
    title: str
    action_type: str
    status: str = "planned"
    dry_run: bool = True
    def validate(self) -> list[str]:
        issues=[]
        if not self.id or not self.title or not self.action_type: issues.append("launch action id, title, and action_type required")
        if self.action_type not in {"announce","deploy_review","traffic_review","monitor","approval","handoff"}: issues.append("invalid action_type")
        if self.status not in {"planned","ready","approved","completed","blocked"}: issues.append("invalid action status")
        if not self.dry_run: issues.append("launch actions must be dry-run by default")
        if any(term in self.title.lower() for term in {"password","token","secret","private key","api key"}): issues.append("launch action metadata may contain sensitive material")
        return issues
    def to_dict(self): return self.__dict__.copy()

@dataclass(frozen=True)
class RollbackPlan:
    id: str
    title: str
    trigger: str
    status: str = "draft"
    dry_run: bool = True
    def validate(self) -> list[str]:
        issues=[]
        if not self.id or not self.title or not self.trigger: issues.append("rollback id, title, and trigger required")
        if self.status not in {"draft","review","approved","archived"}: issues.append("invalid rollback status")
        if not self.dry_run: issues.append("rollback plans must be dry-run by default")
        return issues
    def to_dict(self): return self.__dict__.copy()

@dataclass(frozen=True)
class LaunchAuditEvent:
    id: str
    actor: str
    action: str
    target: str
    payload: dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=now_iso)
    def to_dict(self):
        return {"id": self.id, "actor": self.actor, "action": self.action, "target": self.target, "payload": dict(self.payload), "created_at": self.created_at}
