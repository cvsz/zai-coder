"""No-real-charge safety mode."""

from __future__ import annotations

from .models import PaymentProviderConfig


def no_real_charge_gate(config: PaymentProviderConfig | None = None, payload: dict | None = None) -> dict:
    config = config or PaymentProviderConfig()
    payload = payload or {}
    issues = config.validate()
    if payload.get("mode") and payload.get("mode") != "sandbox":
        issues.append("payload mode must be sandbox")
    if payload.get("live_charge") is True:
        issues.append("live charges are blocked")
    return {"allowed": not issues, "issues": issues, "config": config.to_dict()}


def payment_apply_policy() -> dict:
    return {
        "real_charges_allowed": False,
        "sandbox_only": True,
        "requires_audit": True,
        "requires_no_real_charge_gate": True,
        "allowed_provider_modes": ["sandbox", "stripe_sandbox", "mock"],
    }
