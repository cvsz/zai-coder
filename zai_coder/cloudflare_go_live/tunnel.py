"""Cloudflare Tunnel plan and config renderer."""

from __future__ import annotations

from .models import CloudflareGoLiveConfig, GoLivePlan


def render_tunnel_config(config: CloudflareGoLiveConfig | None = None) -> str:
    config = config or CloudflareGoLiveConfig()
    return f"""# Generated Cloudflare Tunnel config.
# Do not commit credentials JSON.
tunnel: {config.tunnel_name}
credentials-file: /etc/cloudflared/{config.tunnel_name}.json

ingress:
  - hostname: {config.hostname}
    service: {config.local_service_url}
  - service: http_status:404
"""


def tunnel_install_plan(config: CloudflareGoLiveConfig | None = None) -> GoLivePlan:
    config = config or CloudflareGoLiveConfig()
    return GoLivePlan(
        name="cloudflare-tunnel-install-plan",
        steps=(
            "install cloudflared",
            "authenticate cloudflared",
            "create named tunnel",
            "write tunnel config",
            "validate ingress config",
            "run tunnel locally",
            "install cloudflared service",
        ),
        commands=(
            "cloudflared --version",
            "cloudflared tunnel list",
            f"cloudflared tunnel create {config.tunnel_name}",
            f"cloudflared tunnel ingress validate deploy/cloudflare/generated/{config.tunnel_name}.yml",
            f"cloudflared tunnel run {config.tunnel_name}",
        ),
        files={f"deploy/cloudflare/generated/{config.tunnel_name}.yml": render_tunnel_config(config)},
        warnings=(
            "Credentials file must stay outside git.",
            "Use Cloudflare Access before routing public DNS.",
            "Keep app bound to localhost.",
        ),
    )
