"""Per-tenant provider permission policy."""

from __future__ import annotations

from .models import TenantPrincipal
from .isolation import has_tenant_permission


PROVIDER_REQUIREMENTS = {
    "github": "providers:plan",
    "cloudflare": "providers:apply",
    "docker": "providers:apply",
    "postgres": "providers:apply",
}


def provider_permission_decision(principal: TenantPrincipal, provider: str, apply: bool = False) -> dict:
    if provider not in PROVIDER_REQUIREMENTS:
        return {"allowed": False, "reason": f"unknown provider: {provider}"}
    required = "providers:apply" if apply else "providers:plan"
    if not has_tenant_permission(principal, required):
        return {"allowed": False, "reason": f"missing permission: {required}", "provider": provider}
    return {"allowed": True, "reason": "allowed", "provider": provider, "required": required}
