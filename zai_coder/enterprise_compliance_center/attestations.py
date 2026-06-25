"""Policy attestation helpers."""

from __future__ import annotations

import uuid

from .models import PolicyAttestation, now_iso


DEFAULT_POLICIES = [
    {"id": "policy-security", "title": "Security Policy", "required_roles": ["tenant_admin", "operator"]},
    {"id": "policy-data-retention", "title": "Data Retention Policy", "required_roles": ["tenant_admin"]},
    {"id": "policy-incident-response", "title": "Incident Response Policy", "required_roles": ["operator"]},
]


def policy_catalog() -> list[dict]:
    return [dict(policy) for policy in DEFAULT_POLICIES]


def create_attestation(policy_id: str, actor: str, status: str = "pending") -> PolicyAttestation:
    attestation = PolicyAttestation(f"att_{uuid.uuid4().hex[:12]}", policy_id, actor, status, now_iso() if status == "attested" else "")
    issues = attestation.validate()
    if issues:
        raise ValueError("; ".join(issues))
    return attestation


def attestation_gap_report(attestations: list[dict], required_policy_ids: list[str]) -> dict:
    attested = {item["policy_id"] for item in attestations if item["status"] == "attested"}
    missing = [policy_id for policy_id in required_policy_ids if policy_id not in attested]
    return {"ok": not missing, "missing": missing, "attested": sorted(attested)}
