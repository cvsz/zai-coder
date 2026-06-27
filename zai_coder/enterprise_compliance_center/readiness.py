"""Audit readiness gate."""

from __future__ import annotations

from .frameworks import framework_catalog
from .controls import control_library
from .evidence import evidence_gap_report
from .data_register import processing_register_validation
from .attestations import attestation_gap_report
from .risk_matrix import risk_control_matrix


def audit_readiness_gate(evidence: list[dict], attestations: list[dict], approval_id: str = "", execute: bool = False, root: str = ".") -> dict:
    controls = control_library()
    evidence_gaps = evidence_gap_report(controls, evidence, execute=execute, root=root)
    processing = processing_register_validation()
    required_policies = ["policy-security", "policy-data-retention", "policy-incident-response"]
    attestation = attestation_gap_report(attestations, required_policies)
    high_risks = [row for row in risk_control_matrix() if row["level"] in {"high", "critical"}]
    checks = {
        "frameworks_valid": bool(framework_catalog()),
        "controls_valid": bool(controls),
        "evidence_complete": evidence_gaps["ok"],
        "processing_register_valid": processing["ok"],
        "attestations_complete": attestation["ok"],
        "high_risks_reviewed": bool(approval_id.startswith("approved_")) or not high_risks,
    }
    blocked = [name for name, ok in checks.items() if not ok]
    return {
        "allowed": not blocked,
        "blocked": blocked,
        "checks": checks,
        "evidence_gaps": evidence_gaps,
        "processing": processing,
        "attestations": attestation,
        "high_risks": high_risks,
    }


def audit_package_plan(framework_id: str = "soc2") -> dict:
    return {
        "dry_run": True,
        "framework_id": framework_id,
        "steps": [
            "validate framework catalog",
            "validate control library",
            "collect safe evidence inventory",
            "generate evidence gap report",
            "validate processing register",
            "validate policy attestations",
            "review high risks",
            "export audit package without secrets",
        ],
    }
