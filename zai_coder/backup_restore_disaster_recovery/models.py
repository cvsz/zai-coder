from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

@dataclass(frozen=True)
class BackupPlan:
    id: str
    name: str
    target: str
    cadence: str = "daily"
    retention_days: int = 7
    status: str = "draft"
    dry_run: bool = True
    def validate(self) -> list[str]:
        issues=[]
        if not self.id or not self.name or not self.target: issues.append("backup plan id, name, and target required")
        if self.cadence not in {"hourly","daily","weekly","monthly"}: issues.append("invalid cadence")
        try:
            retention = int(self.retention_days)
        except (TypeError, ValueError):
            issues.append("retention_days must be numeric")
            retention = 0
        if retention <= 0: issues.append("retention_days must be > 0")
        if self.status not in {"draft","review","approved","archived"}: issues.append("invalid status")
        if not self.dry_run: issues.append("backup plans must be dry-run by default")
        forbidden={"password","token","secret","private key","api key"}
        if any(term in f"{self.name} {self.target}".lower() for term in forbidden): issues.append("backup metadata may contain sensitive material")
        return issues
    def to_dict(self): return self.__dict__.copy()

@dataclass(frozen=True)
class RestoreDrill:
    id: str
    backup_plan_id: str
    scenario_id: str
    drill_type: str = "preview"
    status: str = "planned"
    dry_run: bool = True
    def validate(self) -> list[str]:
        issues=[]
        if not self.id or not self.backup_plan_id or not self.scenario_id: issues.append("drill id, backup_plan_id, and scenario_id required")
        if self.drill_type not in {"preview","tabletop","sandbox_restore","verification"}: issues.append("invalid drill_type")
        if self.status not in {"planned","running","passed","failed","blocked"}: issues.append("invalid drill status")
        if not self.dry_run: issues.append("restore drills must be preview-only by default")
        return issues
    def to_dict(self): return self.__dict__.copy()

@dataclass(frozen=True)
class RecoveryTarget:
    id: str
    service: str
    rpo_minutes: int
    rto_minutes: int
    priority: str = "normal"
    def validate(self) -> list[str]:
        issues=[]
        if not self.id or not self.service: issues.append("target id and service required")
        for name, value in {"rpo_minutes": self.rpo_minutes, "rto_minutes": self.rto_minutes}.items():
            try:
                numeric = int(value)
            except (TypeError, ValueError):
                issues.append(f"{name} must be numeric")
                numeric = -1
            if numeric < 0: issues.append(f"{name} must be >= 0")
        if self.priority not in {"low","normal","high","critical"}: issues.append("invalid priority")
        return issues
    def to_dict(self): return self.__dict__.copy()

@dataclass(frozen=True)
class DrScenario:
    id: str
    title: str
    scenario_type: str
    severity: str = "medium"
    def validate(self) -> list[str]:
        issues=[]
        if not self.id or not self.title or not self.scenario_type: issues.append("scenario id, title, and scenario_type required")
        if self.scenario_type not in {"data_loss","region_outage","operator_error","deployment_regression","dependency_failure"}: issues.append("invalid scenario_type")
        if self.severity not in {"low","medium","high","critical"}: issues.append("invalid severity")
        return issues
    def to_dict(self): return self.__dict__.copy()

@dataclass(frozen=True)
class DrAuditEvent:
    id: str
    actor: str
    action: str
    target: str
    payload: dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=now_iso)
    def to_dict(self):
        return {"id": self.id, "actor": self.actor, "action": self.action, "target": self.target, "payload": dict(self.payload), "created_at": self.created_at}
