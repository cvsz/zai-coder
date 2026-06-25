"""Deployment wizard plan."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class DeploymentWizardPlan:
    hostname: str
    mode: str = "local-cloudflare"
    steps: list[str] = field(default_factory=list)
    dry_run: bool = True

    def to_dict(self) -> dict:
        return {"hostname": self.hostname, "mode": self.mode, "steps": list(self.steps), "dry_run": self.dry_run}


def build_deployment_plan(hostname: str, mode: str = "local-cloudflare") -> DeploymentWizardPlan:
    if "." not in hostname:
        raise ValueError("hostname must be a DNS name")
    return DeploymentWizardPlan(
        hostname=hostname,
        mode=mode,
        steps=[
            "run tests",
            "run safety scan",
            "create backup",
            "build release artifact",
            "generate Cloudflare tunnel config",
            "install systemd service dry-run",
            "enable Cloudflare Access",
            "start localhost service",
            "verify /healthz",
        ],
    )
