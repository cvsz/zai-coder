"""Cloudflare Access policy checklist."""

from __future__ import annotations

from .models import CloudflareGoLiveConfig, GoLivePlan


def access_policy_checklist(config: CloudflareGoLiveConfig | None = None) -> list[dict]:
    config = config or CloudflareGoLiveConfig()
    return [
        {"area": "application", "item": f"Create Access app for {config.hostname}", "required": True},
        {"area": "identity", "item": "Enable at least one identity provider", "required": True},
        {"area": "policy", "item": "Allow only approved users/groups", "required": True},
        {"area": "policy", "item": "Deny everyone else", "required": True},
        {"area": "session", "item": "Set short session duration for admin surface", "required": True},
        {"area": "mfa", "item": "Require MFA if identity provider supports it", "required": True},
        {"area": "headers", "item": "Verify identity headers before trusting user context", "required": False},
        {"area": "audit", "item": "Review Access logs after first go-live test", "required": True},
    ]


def access_policy_plan(config: CloudflareGoLiveConfig | None = None) -> GoLivePlan:
    config = config or CloudflareGoLiveConfig()
    return GoLivePlan(
        name="cloudflare-access-policy-plan",
        steps=tuple(item["item"] for item in access_policy_checklist(config)),
        commands=(
            "# Configure Cloudflare Access in dashboard/API.",
            f"# Application domain: {config.hostname}",
            "# Enforce allowlist policy before DNS route goes live.",
        ),
        warnings=("Do not create public DNS route until Access policy exists.",),
    )
