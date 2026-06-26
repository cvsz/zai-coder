from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

@dataclass(frozen=True)
class TestCase:
    __test__ = False  # prevent pytest from collecting this dataclass as a test class
    id: str
    name: str
    suite: str
    test_type: str = "unit"
    priority: str = "normal"
    status: str = "planned"
    command: str = "pytest"
    def validate(self) -> list[str]:
        issues=[]
        if not self.id or not self.name or not self.suite or not self.command: issues.append("test id, name, suite, and command required")
        if self.test_type not in {"unit","integration","smoke","contract","security","regression","acceptance"}: issues.append("invalid test_type")
        if self.priority not in {"low","normal","high","critical"}: issues.append("invalid priority")
        if self.status not in {"planned","ready","running","passed","failed","blocked"}: issues.append("invalid status")
        if "--no-verify" in self.command or "skip" in self.command.lower(): issues.append("test command must not bypass validation")
        return issues
    def to_dict(self): return self.__dict__.copy()

@dataclass(frozen=True)
class FixtureSpec:
    id: str
    name: str
    fixture_type: str
    scope: str = "local"
    safe: bool = True
    def validate(self) -> list[str]:
        issues=[]
        if not self.id or not self.name or not self.fixture_type: issues.append("fixture id, name, and fixture_type required")
        if self.fixture_type not in {"json","sqlite","file_tree","mock_service","config"}: issues.append("invalid fixture_type")
        if self.scope not in {"local","test","demo"}: issues.append("invalid scope")
        if not self.safe: issues.append("fixture must be safe by default")
        return issues
    def to_dict(self): return self.__dict__.copy()

@dataclass(frozen=True)
class QualityGate:
    id: str
    name: str
    threshold: float
    metric: str
    required: bool = True
    def validate(self) -> list[str]:
        issues=[]
        if not self.id or not self.name or not self.metric: issues.append("gate id, name, and metric required")
        try:
            threshold = float(self.threshold)
        except (TypeError, ValueError):
            issues.append("threshold must be numeric")
            threshold = 0.0
        if threshold < 0: issues.append("threshold must be >= 0")
        if self.metric not in {"tests_passed","coverage","critical_failures","lint_errors","security_findings"}: issues.append("invalid metric")
        return issues
    def to_dict(self): return self.__dict__.copy()

@dataclass(frozen=True)
class QaAuditEvent:
    id: str
    actor: str
    action: str
    target: str
    payload: dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=now_iso)
    def to_dict(self):
        return {"id": self.id, "actor": self.actor, "action": self.action, "target": self.target, "payload": dict(self.payload), "created_at": self.created_at}
