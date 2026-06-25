"""Cloudflare Tunnel plan for installer."""

from __future__ import annotations

from .config import DeployInstallConfig


def render_cloudflare_tunnel_config(config: DeployInstallConfig | None = None) -> str:
    config = config or DeployInstallConfig()
    return f"""# Generated example. Do not commit credentials.
tunnel: {config.app_name}
credentials-file: /etc/cloudflared/{config.app_name}.json

ingress:
  - hostname: {config.domain}
    service: http://{config.host}:{config.port}
  - service: http_status:404
"""


def cloudflare_plan(config: DeployInstallConfig | None = None) -> dict:
    config = config or DeployInstallConfig()
    return {
        "dry_run": True,
        "hostname": config.domain,
        "commands": [
            "cloudflared tunnel list",
            f"cloudflared tunnel ingress validate deploy/cloudflare/{config.app_name}.yml",
            "# Create Cloudflare Access application in dashboard before exposing publicly.",
            "# Route DNS through Cloudflare only after /healthz and /readyz pass locally.",
        ],
        "files": {f"deploy/cloudflare/{config.app_name}.yml": render_cloudflare_tunnel_config(config)},
    }
