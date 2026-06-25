"""Docker launcher plan."""

from __future__ import annotations

from .config import DeployInstallConfig


def docker_launch_plan(config: DeployInstallConfig | None = None) -> dict:
    config = config or DeployInstallConfig()
    return {
        "dry_run": True,
        "compose_file": config.docker_compose_file,
        "commands": [
            f"docker compose -f {config.docker_compose_file} config",
            f"docker compose -f {config.docker_compose_file} build",
            f"docker compose -f {config.docker_compose_file} up -d",
            f"docker compose -f {config.docker_compose_file} ps",
        ],
        "warnings": [
            "Docker service binds to localhost by default.",
            "Do not expose without Cloudflare Access or equivalent.",
        ],
    }
