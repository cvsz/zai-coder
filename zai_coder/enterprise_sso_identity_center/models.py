from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

@dataclass(frozen=True)
class IdentityProviderPlan:
    id: str
    name: str
    provider_type: str
    protocol: str = "oidc"
    status: str = "draft"
    dry_run: bool = True
    created_at: str = field(default_factory=now_iso)
    def validate(self) -> list[str]:
        issues=[]
        if not self.id or not self.name or not self.provider_type:
            issues.append("provider id, name, and provider_type required")
        if self.provider_type not in {"okta","azure_ad","google_workspace","generic_oidc","saml"}:
            issues.append("invalid provider_type")
        if self.protocol not in {"oidc","saml"}:
            issues.append("invalid protocol")
        if self.status not in {"draft","review","approved","archived"}:
            issues.append("invalid status")
        if not self.dry_run:
            issues.append("identity provider plans must be dry-run by default")
        forbidden={"password","token","secret","client_secret","private key","api key"}
        if any(term in self.name.lower() for term in forbidden):
            issues.append("provider metadata may contain sensitive material")
        return issues
    def to_dict(self): return self.__dict__.copy()

@dataclass(frozen=True)
class ScimMapping:
    id: str
    source_attribute: str
    target_attribute: str
    transform: str = "copy"
    status: str = "draft"
    def validate(self) -> list[str]:
        issues=[]
        if not self.id or not self.source_attribute or not self.target_attribute:
            issues.append("mapping id, source_attribute, and target_attribute required")
        if self.transform not in {"copy","rename","normalize","lowercase","redact","drop"}:
            issues.append("invalid transform")
        if self.status not in {"draft","review","approved","blocked"}:
            issues.append("invalid status")
        return issues
    def to_dict(self): return self.__dict__.copy()

@dataclass(frozen=True)
class OrgPolicy:
    id: str
    title: str
    policy_type: str
    enforcement: str = "review"
    status: str = "draft"
    def validate(self) -> list[str]:
        issues=[]
        if not self.id or not self.title or not self.policy_type:
            issues.append("policy id, title, and policy_type required")
        if self.policy_type not in {"mfa","session","role","domain","joiner_mover_leaver","access_review"}:
            issues.append("invalid policy_type")
        if self.enforcement not in {"review","warn","manual_approval","report_only"}:
            issues.append("invalid enforcement")
        if self.status not in {"draft","review","approved","archived"}:
            issues.append("invalid status")
        return issues
    def to_dict(self): return self.__dict__.copy()

@dataclass(frozen=True)
class AccessReviewItem:
    id: str
    subject_ref: str
    resource: str
    role: str
    decision: str = "pending"
    risk: str = "normal"
    def validate(self) -> list[str]:
        issues=[]
        if not self.id or not self.subject_ref or not self.resource or not self.role:
            issues.append("review id, subject_ref, resource, and role required")
        if self.role not in {"owner","admin","operator","reviewer","viewer","auditor"}:
            issues.append("invalid role")
        if self.decision not in {"pending","approved","remove","change","blocked"}:
            issues.append("invalid decision")
        if self.risk not in {"low","normal","high","critical"}:
            issues.append("invalid risk")
        return issues
    def to_dict(self): return self.__dict__.copy()

@dataclass(frozen=True)
class IdentityAuditEvent:
    id: str
    actor: str
    action: str
    target: str
    payload: dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=now_iso)
    def to_dict(self):
        return {"id": self.id, "actor": self.actor, "action": self.action, "target": self.target, "payload": dict(self.payload), "created_at": self.created_at}
