"""Deployment control center model."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class DeploymentTarget:
    slug: str
    name: str
    target_type: str
    status: str = "planned"
    checks: tuple[str, ...] = field(default_factory=tuple)

    def validate(self) -> list[str]:
        issues = []
        if not self.slug:
            issues.append("missing slug")
        if self.target_type not in {"docker", "systemd", "cloudflare", "github", "local"}:
            issues.append(f"invalid target_type: {self.target_type}")
        if self.status not in {"planned", "ready", "blocked", "deployed", "archived"}:
            issues.append(f"invalid status: {self.status}")
        return issues

    def to_dict(self) -> dict:
        return {
            "slug": self.slug,
            "name": self.name,
            "target_type": self.target_type,
            "status": self.status,
            "checks": list(self.checks),
        }


def default_deployment_targets() -> list[dict]:
    targets = [
        DeploymentTarget("local", "Localhost", "local", "ready", ("healthz", "api-auth")),
        DeploymentTarget("docker", "Docker Compose", "docker", "planned", ("docker-build", "compose-config")),
        DeploymentTarget("systemd", "Systemd Service", "systemd", "planned", ("service-file", "logs")),
        DeploymentTarget("cloudflare", "Cloudflare Tunnel", "cloudflare", "blocked", ("access-policy", "tunnel-config")),
        DeploymentTarget("github", "GitHub Release", "github", "planned", ("gpg-sign", "release-artifact")),
    ]
    return [target.to_dict() for target in targets]
