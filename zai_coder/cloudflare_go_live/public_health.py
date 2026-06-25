"""Public health verification plan."""

from __future__ import annotations

from .models import CloudflareGoLiveConfig, GoLivePlan


def public_health_verification_plan(config: CloudflareGoLiveConfig | None = None) -> GoLivePlan:
    config = config or CloudflareGoLiveConfig()
    return GoLivePlan(
        name="public-health-verification-plan",
        steps=(
            "verify local health",
            "verify local readiness",
            "verify HTTPS endpoint responds",
            "verify Access challenge or authorized response",
            "verify no protected API is public without session",
        ),
        commands=(
            f"curl -fsS {config.local_service_url}/healthz",
            f"curl -fsS {config.local_service_url}/readyz",
            f"curl -I https://{config.hostname}/healthz",
            f"curl -I https://{config.hostname}/api/status",
        ),
        warnings=("Expected protected API behavior is Access challenge or 401/403.",),
    )
