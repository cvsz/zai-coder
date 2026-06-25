"""Ubuntu deploy install plan."""

from __future__ import annotations

from dataclasses import dataclass, field

from .config import DeployInstallConfig


@dataclass(frozen=True)
class InstallPlan:
    name: str
    commands: tuple[str, ...] = field(default_factory=tuple)
    files: dict[str, str] = field(default_factory=dict)
    dry_run: bool = True
    warnings: tuple[str, ...] = ()

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "commands": list(self.commands),
            "files": dict(self.files),
            "dry_run": self.dry_run,
            "warnings": list(self.warnings),
        }


def ubuntu_install_plan(config: DeployInstallConfig | None = None) -> InstallPlan:
    config = config or DeployInstallConfig()
    issues = config.validate()
    packages = " ".join(config.required_runtime_packages)
    return InstallPlan(
        name="ubuntu-24.04-install-plan",
        commands=(
            "sudo apt-get update",
            f"sudo apt-get install -y {packages}",
            f"sudo mkdir -p {config.install_dir}",
            f"sudo chown -R {config.service_user}:{config.service_user} {config.install_dir}",
            "python3 -m venv .venv",
            ".venv/bin/python -m pip install --upgrade pip",
            ".venv/bin/python -m pip install -r requirements-production.txt",
            "make production-migrate-plan",
            "make production-smoke-plan",
        ),
        dry_run=True,
        warnings=tuple(issues) + (
            "Install script is dry-run by default. Set APPLY=1 for mutation.",
            "Review before running on a production host.",
        ),
    )


def one_command_setup_plan(config: DeployInstallConfig | None = None) -> InstallPlan:
    config = config or DeployInstallConfig()
    return InstallPlan(
        name="one-command-setup-plan",
        commands=(
            "./install.sh",
            "make first-run",
            "make deploy-local",
            "make healthcheck",
        ),
        dry_run=True,
        warnings=("Use localhost-first. Add Cloudflare Access before public exposure.",),
    )
