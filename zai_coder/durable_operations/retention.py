"""Retention policies for durable operations artifacts."""

from dataclasses import dataclass
from typing import Dict
from .store import DurableStore

@dataclass
class RetentionPolicy:
    table: str
    retention_days: int

DEFAULT_RETENTION_POLICIES = [
    RetentionPolicy("kpi_snapshots", 365),
    RetentionPolicy("health_trends", 90),
    RetentionPolicy("compliance_evidence", 365 * 7),
    RetentionPolicy("audit_streams", 365 * 2),
    RetentionPolicy("release_evidence", 365 * 10),
]

def apply_retention_policies(store: DurableStore, policies: list[RetentionPolicy] | None = None) -> Dict[str, str]:
    policies = policies or DEFAULT_RETENTION_POLICIES
    results = {}
    for policy in policies:
        try:
            store.apply_retention_policy(policy.table, policy.retention_days)
            results[policy.table] = f"Applied retention of {policy.retention_days} days."
        except Exception as e:
            results[policy.table] = f"Error: {e}"
    return results
