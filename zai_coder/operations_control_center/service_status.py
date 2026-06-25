"""Service status panel plans."""

from __future__ import annotations

from .models import OperationPlan, ServiceStatus


def default_service_statuses() -> list[ServiceStatus]:
    return [
        ServiceStatus("zai-coder-api", "local", "planned", "FastAPI localhost service"),
        ServiceStatus("zai-coder-systemd", "systemd", "planned", "systemd unit"),
        ServiceStatus("zai-coder-docker", "docker", "planned", "Docker Compose profile"),
        ServiceStatus("postgres", "database", "planned", "PostgreSQL backend"),
        ServiceStatus("cloudflare-access", "cloudflare", "blocked", "Enable Access before public DNS"),
    ]


def service_status_plan(service_name: str = "zai-coder-control-plane") -> OperationPlan:
    return OperationPlan(
        name="service-status-plan",
        action="status",
        commands=(
            f"systemctl status {service_name}.service --no-pager",
            "docker compose -f deploy/docker/docker-compose.production-hardening.yml ps",
            "curl -fsS http://127.0.0.1:8765/healthz",
            "curl -fsS http://127.0.0.1:8765/readyz",
        ),
        warnings=("Read-only status plan.",),
    )


def restart_service_plan(service_name: str = "zai-coder-control-plane") -> OperationPlan:
    return OperationPlan(
        name="restart-service-plan",
        action="restart",
        commands=(
            f"sudo systemctl restart {service_name}.service",
            f"sudo systemctl status {service_name}.service --no-pager",
            "make healthcheck",
        ),
        requires_backup=False,
        warnings=("Dry-run by default. Use APPLY=1 only after checking status.",),
    )
