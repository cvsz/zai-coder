"""Payment provider environment validation."""

from __future__ import annotations


PAYMENT_ENV_REQUIREMENTS = {
    "sandbox": (),
    "mock": (),
    "stripe_sandbox": ("STRIPE_SANDBOX_SECRET_KEY", "STRIPE_SANDBOX_WEBHOOK_SECRET"),
}


def validate_payment_env(provider: str = "sandbox", env: dict[str, str] | None = None) -> dict:
    env = env or {}
    if provider not in PAYMENT_ENV_REQUIREMENTS:
        return {"ok": False, "provider": provider, "missing": [], "issues": [f"unknown payment provider: {provider}"], "safe_env_keys": sorted(env.keys())}
    missing = [name for name in PAYMENT_ENV_REQUIREMENTS[provider] if not env.get(name)]
    issues = []
    for key in env:
        if key.startswith("STRIPE_LIVE_") or key in {"STRIPE_SECRET_KEY", "STRIPE_WEBHOOK_SECRET"}:
            issues.append(f"live payment env key is not allowed in sandbox: {key}")
    return {"ok": not missing and not issues, "provider": provider, "missing": missing, "issues": issues, "safe_env_keys": sorted(env.keys())}
