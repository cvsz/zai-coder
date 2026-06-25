from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

@dataclass(frozen=True)
class DataSourceSpec:
    id: str
    name: str
    source_type: str
    location: str
    mode: str = "read_only"
    status: str = "planned"
    def validate(self) -> list[str]:
        issues=[]
        if not self.id or not self.name or not self.source_type or not self.location:
            issues.append("source id, name, source_type, and location required")
        if self.source_type not in {"json","csv","sqlite","postgres_plan","file_tree","api_snapshot"}:
            issues.append("invalid source_type")
        if self.mode not in {"read_only","export_only","plan_only"}:
            issues.append("invalid mode")
        if self.status not in {"planned","validated","blocked","archived"}:
            issues.append("invalid source status")
        forbidden={"password","token","secret","private key","api key"}
        if any(term in f"{self.name} {self.location}".lower() for term in forbidden):
            issues.append("source metadata may contain sensitive material")
        return issues
    def to_dict(self): return self.__dict__.copy()

@dataclass(frozen=True)
class MigrationJob:
    id: str
    title: str
    source_id: str
    target: str
    job_type: str = "migration_plan"
    status: str = "draft"
    dry_run: bool = True
    created_at: str = field(default_factory=now_iso)
    def validate(self) -> list[str]:
        issues=[]
        if not self.id or not self.title or not self.source_id or not self.target:
            issues.append("job id, title, source_id, and target required")
        if self.job_type not in {"import_plan","export_plan","migration_plan","schema_check","rollback_preview"}:
            issues.append("invalid job_type")
        if self.status not in {"draft","review","approved","completed","blocked"}:
            issues.append("invalid job status")
        if not self.dry_run:
            issues.append("migration jobs must be dry-run by default")
        return issues
    def to_dict(self): return self.__dict__.copy()

@dataclass(frozen=True)
class SchemaField:
    id: str
    dataset: str
    name: str
    field_type: str
    required: bool = False
    def validate(self) -> list[str]:
        issues=[]
        if not self.id or not self.dataset or not self.name or not self.field_type:
            issues.append("schema field id, dataset, name, and field_type required")
        if self.field_type not in {"string","integer","float","boolean","datetime","json"}:
            issues.append("invalid field_type")
        return issues
    def to_dict(self): return self.__dict__.copy()

@dataclass(frozen=True)
class DataMapping:
    id: str
    source_field: str
    target_field: str
    transform: str = "copy"
    status: str = "planned"
    def validate(self) -> list[str]:
        issues=[]
        if not self.id or not self.source_field or not self.target_field:
            issues.append("mapping id, source_field, and target_field required")
        if self.transform not in {"copy","rename","cast","normalize","drop","redact"}:
            issues.append("invalid transform")
        if self.status not in {"planned","validated","blocked"}:
            issues.append("invalid mapping status")
        return issues
    def to_dict(self): return self.__dict__.copy()

@dataclass(frozen=True)
class MigrationAuditEvent:
    id: str
    actor: str
    action: str
    target: str
    payload: dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=now_iso)
    def to_dict(self):
        return {"id": self.id, "actor": self.actor, "action": self.action, "target": self.target, "payload": dict(self.payload), "created_at": self.created_at}
