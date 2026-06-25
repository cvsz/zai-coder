"""First-run bootstrap plan."""

from __future__ import annotations

from .config import DeployInstallConfig


def first_run_plan(admin_email: str = "admin@example.com", config: DeployInstallConfig | None = None) -> dict:
    config = config or DeployInstallConfig()
    if "@" not in admin_email:
        raise ValueError("admin_email must be valid")
    return {
        "dry_run": True,
        "admin_email": admin_email,
        "steps": [
            "create .env from .env.example",
            "generate local session secret",
            "run migrations",
            "bootstrap admin session/API key",
            "start localhost service",
            "verify /healthz",
            "verify /readyz",
            "generate production smoke plan",
        ],
        "commands": [
            "cp .env.example .env",
            "make production-migrate-plan",
            "make production-migrate-apply APPLY=1",
            f"make admin-bootstrap APPLY=1 ADMIN_EMAIL={admin_email}",
            "make serve-fastapi",
            "make healthcheck",
        ],
    }
