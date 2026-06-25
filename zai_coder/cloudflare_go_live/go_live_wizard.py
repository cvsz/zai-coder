"""Local-to-public go-live wizard."""

from __future__ import annotations

from .models import CloudflareGoLiveConfig, GoLivePlan
from .hostname_validator import validate_hostname
from .tunnel import render_tunnel_config
from .access_policy import access_policy_checklist


def go_live_wizard_plan(config: CloudflareGoLiveConfig | None = None) -> GoLivePlan:
    config = config or CloudflareGoLiveConfig()
    validation = validate_hostname(config.hostname)
    warnings = []
    if not validation["ok"]:
        warnings.extend(validation["issues"])
    warnings.extend([
        "Run every step as dry-run first.",
        "Enable Cloudflare Access before DNS route.",
        "Keep app bound to localhost.",
    ])
    return GoLivePlan(
        name="cloudflare-go-live-wizard",
        steps=(
            "validate hostname",
            "verify localhost health",
            "generate tunnel config",
            "create/validate tunnel",
            "create Cloudflare Access application",
            "create Access allow policy",
            "route DNS to tunnel",
            "verify public health",
            "verify protected API is not public",
            "record rollback plan",
        ),
        commands=(
            "make healthcheck",
            "make cloudflare-tunnel-plan",
            "make cloudflare-access-checklist",
            "make cloudflare-dns-plan",
            "make cloudflare-public-health-plan",
            "make cloudflare-dns-rollback-plan",
        ),
        files={f"deploy/cloudflare/generated/{config.tunnel_name}.yml": render_tunnel_config(config)},
        warnings=tuple(warnings),
    )
