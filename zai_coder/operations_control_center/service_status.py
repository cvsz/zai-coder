"""Service status panel plans."""

from __future__ import annotations

from .models import OperationPlan, ServiceStatus


def default_service_statuses(execute: bool = False) -> list[ServiceStatus]:
    statuses = [
        ServiceStatus("zai-coder-api", "local", "planned", "FastAPI localhost service"),
        ServiceStatus("zai-coder-systemd", "systemd", "planned", "systemd unit"),
        ServiceStatus("zai-coder-docker", "docker", "planned", "Docker Compose profile"),
        ServiceStatus("postgres", "database", "planned", "PostgreSQL backend"),
        ServiceStatus("cloudflare-access", "cloudflare", "blocked", "Enable Access before public DNS"),
    ]
    if execute:
        import subprocess
        live_statuses = []
        for s in statuses:
            live_status = s.status
            detail = s.detail
            if s.target == "systemd":
                try:
                    res = subprocess.run(["systemctl", "is-active", s.name], capture_output=True, text=True)
                    live_status = "running" if res.returncode == 0 else "stopped"
                    detail = res.stdout.strip() or "systemd status checked"
                except Exception:
                    live_status = "unknown"
            elif s.target == "docker":
                try:
                    res = subprocess.run(["docker", "ps", "-q", "-f", f"name={s.name}"], capture_output=True, text=True)
                    live_status = "running" if res.stdout.strip() else "stopped"
                    detail = "docker status checked"
                except Exception:
                    live_status = "unknown"
            
            live_statuses.append(ServiceStatus(s.name, s.target, live_status, detail))
        return live_statuses
    return statuses


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
