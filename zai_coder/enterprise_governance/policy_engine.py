"""Governance policy engine."""

from __future__ import annotations

from zai_coder.core.booleans import coerce_bool
from .models import GovernancePolicy, GovernanceDecision


DEFAULT_POLICIES = [
    GovernancePolicy(
        id="gov-001",
        name="Dry-run first",
        description="All mutating operations must expose a dry-run plan first.",
        severity="critical",
        controls=("dry_run", "approval"),
    ),
    GovernancePolicy(
        id="gov-002",
        name="Approval required for apply",
        description="External mutation requires approval id.",
        severity="critical",
        controls=("approval", "audit"),
    ),
    GovernancePolicy(
        id="gov-003",
        name="Secrets outside repository",
        description="Secrets must not be committed.",
        severity="critical",
        controls=("secret_scan", "repo_check"),
    ),
    GovernancePolicy(
        id="gov-004",
        name="Cloudflare Access before public exposure",
        description="Public go-live requires Access policy.",
        severity="high",
        controls=("cloudflare_access", "exposure_scan"),
    ),
]


def policy_manifest() -> list[dict]:
    return [policy.to_dict() for policy in DEFAULT_POLICIES]


def evaluate_operation(payload: dict, policies: list[GovernancePolicy] | None = None) -> list[GovernanceDecision]:
    policies = policies or DEFAULT_POLICIES
    decisions: list[GovernanceDecision] = []
    mutating = coerce_bool(payload.get("mutating", False))
    apply = coerce_bool(payload.get("apply", False))
    approval_id = payload.get("approval_id", "")
    public_exposure = coerce_bool(payload.get("public_exposure", False))
    access_enabled = coerce_bool(payload.get("cloudflare_access_enabled", False))
    dry_run_completed = coerce_bool(payload.get("dry_run_completed", False))
    secret_scan_ok = coerce_bool(payload.get("secret_scan_ok", True), default=True)

    for policy in policies:
        if policy.id == "gov-001" and mutating and apply and not dry_run_completed:
            decisions.append(GovernanceDecision(False, policy.id, "mutating apply requires prior dry-run", policy.severity, True))
        elif policy.id == "gov-002" and apply and not str(approval_id).startswith("approved_"):
            decisions.append(GovernanceDecision(False, policy.id, "apply requires approval id", policy.severity, True))
        elif policy.id == "gov-003" and not secret_scan_ok:
            decisions.append(GovernanceDecision(False, policy.id, "secret scan must pass", policy.severity, True))
        elif policy.id == "gov-004" and public_exposure and not access_enabled:
            decisions.append(GovernanceDecision(False, policy.id, "Cloudflare Access required before public exposure", policy.severity, True))
        else:
            decisions.append(GovernanceDecision(True, policy.id, "policy satisfied", policy.severity, False))
    return decisions


def governance_gate(payload: dict) -> dict:
    decisions = evaluate_operation(payload)
    blocked = [d.to_dict() for d in decisions if not d.allowed]
    return {"allowed": not blocked, "blocked": blocked, "decisions": [d.to_dict() for d in decisions]}
