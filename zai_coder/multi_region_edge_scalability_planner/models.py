from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

@dataclass(frozen=True)
class RegionSpec:
    id: str
    name: str
    region_code: str
    role: str = "secondary"
    status: str = "planned"
    data_residency: str = "review"
    def validate(self) -> list[str]:
        issues=[]
        if not self.id or not self.name or not self.region_code:
            issues.append("region id, name, and region_code required")
        if self.role not in {"primary","secondary","edge","standby"}:
            issues.append("invalid region role")
        if self.status not in {"planned","review","ready","blocked","archived"}:
            issues.append("invalid region status")
        if self.data_residency not in {"review","allowed","restricted","not_applicable"}:
            issues.append("invalid data_residency")
        return issues
    def to_dict(self): return self.__dict__.copy()

@dataclass(frozen=True)
class EdgeRoutePlan:
    id: str
    hostname: str
    strategy: str
    primary_region: str
    fallback_region: str = ""
    status: str = "draft"
    dry_run: bool = True
    def validate(self) -> list[str]:
        issues=[]
        if not self.id or not self.hostname or not self.strategy or not self.primary_region:
            issues.append("route id, hostname, strategy, and primary_region required")
        if self.strategy not in {"geo","latency","weighted","failover","single_region"}:
            issues.append("invalid strategy")
        if self.status not in {"draft","review","approved","blocked"}:
            issues.append("invalid route status")
        if not self.dry_run:
            issues.append("edge route plans must be dry-run by default")
        forbidden={"password","token","secret","private key","api key"}
        if any(term in self.hostname.lower() for term in forbidden):
            issues.append("route metadata may contain sensitive material")
        return issues
    def to_dict(self): return self.__dict__.copy()

@dataclass(frozen=True)
class CapacityModel:
    id: str
    service: str
    baseline_rps: int
    peak_rps: int
    headroom_percent: int = 30
    status: str = "draft"
    def validate(self) -> list[str]:
        issues=[]
        if not self.id or not self.service:
            issues.append("capacity id and service required")
        for name, value in {"baseline_rps": self.baseline_rps, "peak_rps": self.peak_rps, "headroom_percent": self.headroom_percent}.items():
            try:
                numeric = int(value)
            except (TypeError, ValueError):
                issues.append(f"{name} must be numeric")
                numeric = -1
            if numeric < 0:
                issues.append(f"{name} must be >= 0")
        if self.status not in {"draft","review","approved","blocked"}:
            issues.append("invalid capacity status")
        return issues
    def to_dict(self): return self.__dict__.copy()

@dataclass(frozen=True)
class LatencyBudget:
    id: str
    user_region: str
    target_ms: int
    p95_ms: int
    status: str = "planned"
    def validate(self) -> list[str]:
        issues=[]
        if not self.id or not self.user_region:
            issues.append("latency budget id and user_region required")
        for name, value in {"target_ms": self.target_ms, "p95_ms": self.p95_ms}.items():
            try:
                numeric = int(value)
            except (TypeError, ValueError):
                issues.append(f"{name} must be numeric")
                numeric = -1
            if numeric < 0:
                issues.append(f"{name} must be >= 0")
        if self.status not in {"planned","met","at_risk","missed"}:
            issues.append("invalid latency budget status")
        return issues
    def to_dict(self): return self.__dict__.copy()

@dataclass(frozen=True)
class ScalingScenario:
    id: str
    title: str
    scenario_type: str
    severity: str = "medium"
    dry_run: bool = True
    def validate(self) -> list[str]:
        issues=[]
        if not self.id or not self.title or not self.scenario_type:
            issues.append("scenario id, title, and scenario_type required")
        if self.scenario_type not in {"traffic_spike","region_failover","edge_cache_pressure","database_hotspot","queue_backlog"}:
            issues.append("invalid scenario_type")
        if self.severity not in {"low","medium","high","critical"}:
            issues.append("invalid severity")
        if not self.dry_run:
            issues.append("scaling scenarios must be dry-run by default")
        return issues
    def to_dict(self): return self.__dict__.copy()

@dataclass(frozen=True)
class ScalabilityAuditEvent:
    id: str
    actor: str
    action: str
    target: str
    payload: dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=now_iso)
    def to_dict(self):
        return {"id": self.id, "actor": self.actor, "action": self.action, "target": self.target, "payload": dict(self.payload), "created_at": self.created_at}
