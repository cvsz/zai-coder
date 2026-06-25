from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

@dataclass(frozen=True)
class ReleaseArtifact:
    id: str
    name: str
    artifact_type: str
    path: str
    required: bool = True
    status: str = "ready"
    def validate(self) -> list[str]:
        issues=[]
        if not self.id or not self.name or not self.artifact_type or not self.path: issues.append("artifact id, name, artifact_type, and path required")
        if self.artifact_type not in {"installer","docs","dashboard","test_report","security_report","privacy_report","compliance_report","migration_guide","rollback_guide","release_notes","validation_report","hermes_alignment"}: issues.append("invalid artifact_type")
        if self.status not in {"ready","review","missing","archived"}: issues.append("invalid artifact status")
        if any(term in self.path.lower() for term in {"secret","private key","api key","password","token"}): issues.append("artifact path may contain sensitive material")
        return issues
    def to_dict(self): return self.__dict__.copy()

@dataclass(frozen=True)
class FinalValidationGate:
    id: str
    title: str
    category: str
    status: str = "pending"
    required: bool = True
    def validate(self) -> list[str]:
        issues=[]
        if not self.id or not self.title or not self.category: issues.append("gate id, title, and category required")
        if self.category not in {"install","test","security","privacy","compliance","docs","go_live","rollback","hermes_alignment"}: issues.append("invalid category")
        if self.status not in {"passed","pending","failed","waived","blocked"}: issues.append("invalid gate status")
        return issues
    def to_dict(self): return self.__dict__.copy()

@dataclass(frozen=True)
class HermesAlignmentItem:
    id: str
    title: str
    pattern: str
    adopted: bool = True
    safety_note: str = "local-first and review-first"
    def validate(self) -> list[str]:
        issues=[]
        if not self.id or not self.title or not self.pattern: issues.append("alignment id, title, and pattern required")
        if self.pattern not in {"learning_loop","memory","skills","context_files","mcp_toolsets","terminal_backends","checkpoints_rollback","security_approvals","messaging_gateway","delegation"}: issues.append("invalid Hermes alignment pattern")
        if not self.safety_note: issues.append("safety_note required")
        return issues
    def to_dict(self): return self.__dict__.copy()

@dataclass(frozen=True)
class FinalReleaseAuditEvent:
    id: str
    actor: str
    action: str
    target: str
    payload: dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=now_iso)
    def to_dict(self):
        return {"id": self.id, "actor": self.actor, "action": self.action, "target": self.target, "payload": dict(self.payload), "created_at": self.created_at}
