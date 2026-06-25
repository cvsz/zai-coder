from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

@dataclass(frozen=True)
class ThreatSignal:
    id: str
    title: str
    signal_type: str
    source: str
    severity: str = "medium"
    status: str = "open"
    created_at: str = field(default_factory=now_iso)
    def validate(self) -> list[str]:
        issues=[]
        if not self.id or not self.title or not self.signal_type or not self.source:
            issues.append("signal id, title, signal_type, and source required")
        if self.signal_type not in {"auth_anomaly","policy_drift","dependency_alert","config_risk","data_access","availability"}:
            issues.append("invalid signal_type")
        if self.severity not in {"low","medium","high","critical"}:
            issues.append("invalid severity")
        if self.status not in {"open","triaged","monitoring","resolved","false_positive"}:
            issues.append("invalid signal status")
        forbidden={"password","token","secret","private key","api key"}
        if any(term in f"{self.title} {self.source}".lower() for term in forbidden):
            issues.append("signal metadata may contain sensitive material")
        return issues
    def to_dict(self): return self.__dict__.copy()

@dataclass(frozen=True)
class PolicyAlert:
    id: str
    policy_id: str
    title: str
    severity: str = "medium"
    action: str = "review"
    status: str = "open"
    def validate(self) -> list[str]:
        issues=[]
        if not self.id or not self.policy_id or not self.title:
            issues.append("alert id, policy_id, and title required")
        if self.severity not in {"low","medium","high","critical"}:
            issues.append("invalid alert severity")
        if self.action not in {"review","notify_owner","create_incident_plan","monitor"}:
            issues.append("invalid alert action")
        if self.status not in {"open","in_review","resolved","suppressed"}:
            issues.append("invalid alert status")
        return issues
    def to_dict(self): return self.__dict__.copy()

@dataclass(frozen=True)
class IncidentPlan:
    id: str
    title: str
    incident_type: str
    severity: str = "medium"
    status: str = "draft"
    dry_run: bool = True
    created_at: str = field(default_factory=now_iso)
    def validate(self) -> list[str]:
        issues=[]
        if not self.id or not self.title or not self.incident_type:
            issues.append("incident plan id, title, and incident_type required")
        if self.incident_type not in {"access_review","policy_drift","service_risk","data_review","availability_review"}:
            issues.append("invalid incident_type")
        if self.severity not in {"low","medium","high","critical"}:
            issues.append("invalid incident severity")
        if self.status not in {"draft","review","approved","closed","blocked"}:
            issues.append("invalid incident status")
        if not self.dry_run:
            issues.append("incident workflows must be plan-only by default")
        return issues
    def to_dict(self): return self.__dict__.copy()

@dataclass(frozen=True)
class SecurityEvidence:
    id: str
    evidence_type: str
    title: str
    redacted: bool = True
    status: str = "ready"
    def validate(self) -> list[str]:
        issues=[]
        if not self.id or not self.evidence_type or not self.title:
            issues.append("evidence id, evidence_type, and title required")
        if self.evidence_type not in {"signal_summary","alert_summary","incident_plan","policy_snapshot","risk_score"}:
            issues.append("invalid evidence_type")
        if self.status not in {"ready","review","archived"}:
            issues.append("invalid evidence status")
        if not self.redacted:
            issues.append("security evidence must be redacted by default")
        return issues
    def to_dict(self): return self.__dict__.copy()

@dataclass(frozen=True)
class SecurityAuditEvent:
    id: str
    actor: str
    action: str
    target: str
    payload: dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=now_iso)
    def to_dict(self):
        return {"id": self.id, "actor": self.actor, "action": self.action, "target": self.target, "payload": dict(self.payload), "created_at": self.created_at}
