"""Enterprise Compliance Center models.

This package provides compliance planning, control mapping, evidence inventory,
and audit readiness gates. It does not provide legal advice or certify
compliance automatically.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass(frozen=True)
class ComplianceFramework:
    id: str
    name: str
    version: str
    jurisdiction: str = "global"
    description: str = ""
    control_domains: tuple[str, ...] = ()
    created_at: str = field(default_factory=now_iso)

    def validate(self) -> list[str]:
        issues: list[str] = []
        if not self.id or not self.name or not self.version:
            issues.append("framework id, name, and version required")
        if "/" in self.id or ".." in self.id:
            issues.append("unsafe framework id")
        if not self.control_domains:
            issues.append("framework requires at least one control domain")
        return issues

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "version": self.version,
            "jurisdiction": self.jurisdiction,
            "description": self.description,
            "control_domains": list(self.control_domains),
            "created_at": self.created_at,
        }


@dataclass(frozen=True)
class ComplianceControl:
    id: str
    framework_id: str
    domain: str
    title: str
    description: str
    owner: str = "compliance-owner"
    status: str = "planned"
    evidence_required: tuple[str, ...] = ()

    def validate(self) -> list[str]:
        issues: list[str] = []
        if not self.id or not self.framework_id or not self.title:
            issues.append("control id, framework_id, and title required")
        if self.status not in {"planned", "implemented", "monitored", "gap", "accepted_risk"}:
            issues.append("invalid control status")
        if not self.evidence_required:
            issues.append("control requires evidence list")
        return issues

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "framework_id": self.framework_id,
            "domain": self.domain,
            "title": self.title,
            "description": self.description,
            "owner": self.owner,
            "status": self.status,
            "evidence_required": list(self.evidence_required),
        }


@dataclass(frozen=True)
class EvidenceItem:
    id: str
    control_id: str
    title: str
    source_path: str
    evidence_type: str = "document"
    collected_by: str = "system"
    contains_secret: bool = False
    collected_at: str = field(default_factory=now_iso)

    def validate(self) -> list[str]:
        issues: list[str] = []
        if not self.id or not self.control_id or not self.title:
            issues.append("evidence id, control_id, and title required")
        if self.evidence_type not in {"document", "log", "screenshot", "config", "report", "attestation"}:
            issues.append("invalid evidence_type")
        if self.contains_secret:
            issues.append("evidence containing secrets cannot be exported")
        if any(part in self.source_path for part in [".env", "credentials", "secret", ".git/"]):
            issues.append("evidence source path may contain sensitive material")
        return issues

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "control_id": self.control_id,
            "title": self.title,
            "source_path": self.source_path,
            "evidence_type": self.evidence_type,
            "collected_by": self.collected_by,
            "contains_secret": self.contains_secret,
            "collected_at": self.collected_at,
        }


@dataclass(frozen=True)
class DataProcessingRecord:
    id: str
    system: str
    data_category: str
    purpose: str
    retention_days: int
    lawful_basis: str = "legitimate_interest"
    region: str = "global"
    pii: bool = False
    created_at: str = field(default_factory=now_iso)

    def validate(self) -> list[str]:
        issues: list[str] = []
        if not self.id or not self.system or not self.data_category or not self.purpose:
            issues.append("processing record id, system, data_category, and purpose required")
        if self.retention_days < 0:
            issues.append("retention_days must be >= 0")
        if self.pii and self.retention_days == 0:
            issues.append("PII record requires explicit retention period")
        return issues

    def to_dict(self) -> dict:
        return self.__dict__.copy()


@dataclass(frozen=True)
class PolicyAttestation:
    id: str
    policy_id: str
    actor: str
    status: str = "pending"
    attested_at: str = ""

    def validate(self) -> list[str]:
        issues: list[str] = []
        if not self.id or not self.policy_id or not self.actor:
            issues.append("attestation id, policy_id, and actor required")
        if self.status not in {"pending", "attested", "declined", "expired"}:
            issues.append("invalid attestation status")
        return issues

    def to_dict(self) -> dict:
        return self.__dict__.copy()


@dataclass(frozen=True)
class ComplianceAuditEvent:
    id: str
    actor: str
    action: str
    target: str
    payload: dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=now_iso)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "actor": self.actor,
            "action": self.action,
            "target": self.target,
            "payload": dict(self.payload),
            "created_at": self.created_at,
        }
