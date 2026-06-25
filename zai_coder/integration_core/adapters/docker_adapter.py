"""Docker integration adapter."""

from __future__ import annotations

from zai_coder.integration_core.models import IntegrationPlan


def docker_status_plan() -> IntegrationPlan:
    return IntegrationPlan(
        provider="docker",
        action="status",
        commands=[
            "docker version",
            "docker compose version",
            "docker ps --format 'table {{.Names}}\\t{{.Status}}\\t{{.Ports}}'",
        ],
    )


def compose_check_plan(compose_file: str = "docker-compose.yml") -> IntegrationPlan:
    return IntegrationPlan(
        provider="docker",
        action="compose_check",
        commands=[f"docker compose -f {compose_file} config"],
        payload={"compose_file": compose_file},
    )


def image_build_plan(image: str = "zai-coder:local") -> IntegrationPlan:
    return IntegrationPlan(
        provider="docker",
        action="image_build",
        commands=[f"docker build -t {image} ."],
        payload={"image": image},
        warnings=["Build only after tests pass. Do not mount secrets into build context."],
    )


def safe_cleanup_plan() -> IntegrationPlan:
    return IntegrationPlan(
        provider="docker",
        action="safe_cleanup",
        commands=["docker system df", "docker container prune", "docker image prune"],
        warnings=["Volume deletion is intentionally excluded.", "Never run docker system prune --volumes from this adapter."],
    )
