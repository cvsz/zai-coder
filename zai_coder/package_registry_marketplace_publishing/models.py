from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

@dataclass(frozen=True)
class RegistryPackage:
    id: str
    name: str
    package_type: str
    version: str
    description: str
    license_id: str = "MIT"
    visibility: str = "private"
    status: str = "draft"
    created_at: str = field(default_factory=now_iso)
    def validate(self) -> list[str]:
        issues=[]
        if not self.id or not self.name or not self.package_type or not self.version: issues.append("package id, name, package_type, and version required")
        if self.package_type not in {"agent","skill","plugin","template","connector","bundle"}: issues.append("invalid package_type")
        if self.visibility not in {"private","workspace","public"}: issues.append("invalid visibility")
        if self.status not in {"draft","review","approved","published","archived"}: issues.append("invalid package status")
        if not self.version.startswith("v"): issues.append("version must start with v")
        forbidden = {"password","token","secret","api key","private key"}
        if any(term in f"{self.name} {self.description}".lower() for term in forbidden): issues.append("package metadata may contain sensitive material")
        return issues
    def to_dict(self): return self.__dict__.copy()

@dataclass(frozen=True)
class MarketplaceSubmission:
    id: str
    package_id: str
    target: str = "internal-marketplace"
    status: str = "draft"
    notes: str = ""
    dry_run: bool = True
    created_at: str = field(default_factory=now_iso)
    def validate(self) -> list[str]:
        issues=[]
        if not self.id or not self.package_id or not self.target: issues.append("submission id, package_id, and target required")
        if self.status not in {"draft","review","approved","rejected","submitted"}: issues.append("invalid submission status")
        if self.target not in {"internal-marketplace","github-release","plugin-hub","customer-catalog"}: issues.append("invalid target")
        if not self.dry_run: issues.append("marketplace submissions must be dry-run by default")
        return issues
    def to_dict(self): return self.__dict__.copy()

@dataclass(frozen=True)
class CompatibilityRecord:
    id: str
    package_id: str
    runtime: str
    min_version: str
    max_version: str = ""
    status: str = "compatible"
    def validate(self) -> list[str]:
        issues=[]
        if not self.id or not self.package_id or not self.runtime or not self.min_version: issues.append("compatibility fields required")
        if self.status not in {"compatible","needs_review","blocked"}: issues.append("invalid compatibility status")
        if not self.min_version.startswith("v"): issues.append("min_version must start with v")
        return issues
    def to_dict(self): return self.__dict__.copy()

@dataclass(frozen=True)
class LicenseAttribution:
    id: str
    package_id: str
    license_id: str
    attribution: str
    review_status: str = "pending"
    def validate(self) -> list[str]:
        issues=[]
        if not self.id or not self.package_id or not self.license_id: issues.append("license attribution fields required")
        if self.review_status not in {"pending","approved","needs_changes","blocked"}: issues.append("invalid review_status")
        if self.license_id not in {"MIT","Apache-2.0","BSD-3-Clause","MPL-2.0","Proprietary-Internal"}: issues.append("unsupported license")
        return issues
    def to_dict(self): return self.__dict__.copy()

@dataclass(frozen=True)
class MarketplaceAuditEvent:
    id: str
    actor: str
    action: str
    target: str
    payload: dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=now_iso)
    def to_dict(self):
        return {"id": self.id, "actor": self.actor, "action": self.action, "target": self.target, "payload": dict(self.payload), "created_at": self.created_at}
