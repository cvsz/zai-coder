"""DNS record planner and rollback plan."""

from __future__ import annotations

from .models import CloudflareGoLiveConfig, GoLivePlan


def dns_record_plan(config: CloudflareGoLiveConfig | None = None) -> GoLivePlan:
    config = config or CloudflareGoLiveConfig()
    target = f"{config.tunnel_name}.cfargotunnel.com"
    return GoLivePlan(
        name="cloudflare-dns-record-plan",
        steps=(
            "confirm Access policy exists",
            "create proxied CNAME to tunnel",
            "verify DNS propagation",
            "verify Access login challenge",
            "verify public health route",
        ),
        commands=(
            f"cloudflared tunnel route dns {config.tunnel_name} {config.hostname}",
            f"dig +short {config.hostname}",
            f"curl -I https://{config.hostname}/healthz",
        ),
        files={
            "dns_record.json": f'{{"type":"CNAME","name":"{config.hostname}","content":"{target}","proxied":true}}'
        },
        warnings=("Rollback DNS if public health verification fails.",),
    )


def dns_rollback_plan(config: CloudflareGoLiveConfig | None = None) -> GoLivePlan:
    config = config or CloudflareGoLiveConfig()
    return GoLivePlan(
        name="cloudflare-dns-rollback-plan",
        steps=(
            "disable or delete CNAME route",
            "stop cloudflared service if needed",
            "keep localhost service running for investigation",
            "review Access and tunnel logs",
        ),
        commands=(
            f"# Remove DNS route for {config.hostname} in Cloudflare dashboard/API.",
            f"sudo systemctl stop cloudflared || true",
            f"curl -fsS {config.local_service_url}/healthz",
        ),
        warnings=("Do not delete local backups during rollback.",),
    )
