"""Deploy installer configuration models."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True)
class DeployInstallConfig:
    app_name: str = "zai-coder-control-plane"
    install_dir: str = "/opt/zai-coder-control-plane"
    service_user: str = "zai"
    host: str = "127.0.0.1"
    port: int = 8765
    python_bin: str = "python3"
    env_file: str = ".env"
    domain: str = "zai.example.com"
    backup_dir: str = "backups"
    data_dir: str = "data"
    logs_dir: str = "logs"
    storage_dir: str = "storage"
    docker_compose_file: str = "deploy/docker/docker-compose.production-hardening.yml"
    allowed_mutation_env: str = "APPLY"
    required_runtime_packages: tuple[str, ...] = ("python3", "python3-venv", "python3-pip", "curl", "ca-certificates")

    def validate(self) -> list[str]:
        issues: list[str] = []
        if not self.app_name:
            issues.append("app_name required")
        if not self.install_dir.startswith("/opt/"):
            issues.append("install_dir should live under /opt for production installs")
        if self.host not in {"127.0.0.1", "localhost"}:
            issues.append("host must be localhost-first by default")
        if not (1 <= int(self.port) <= 65535):
            issues.append("port must be 1..65535")
        if "." not in self.domain:
            issues.append("domain should be a DNS name")
        return issues

    def to_dict(self) -> dict:
        return {
            "app_name": self.app_name,
            "install_dir": self.install_dir,
            "service_user": self.service_user,
            "host": self.host,
            "port": self.port,
            "python_bin": self.python_bin,
            "env_file": self.env_file,
            "domain": self.domain,
            "backup_dir": self.backup_dir,
            "data_dir": self.data_dir,
            "logs_dir": self.logs_dir,
            "storage_dir": self.storage_dir,
            "docker_compose_file": self.docker_compose_file,
            "required_runtime_packages": list(self.required_runtime_packages),
        }


def default_config() -> DeployInstallConfig:
    return DeployInstallConfig()
