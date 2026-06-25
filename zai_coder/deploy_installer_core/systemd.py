"""Systemd install plan and unit renderer."""

from __future__ import annotations

from .config import DeployInstallConfig


def render_systemd_unit(config: DeployInstallConfig | None = None) -> str:
    config = config or DeployInstallConfig()
    return f"""[Unit]
Description=ZAI Coder Control Plane
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User={config.service_user}
WorkingDirectory={config.install_dir}
EnvironmentFile={config.install_dir}/{config.env_file}
ExecStart={config.install_dir}/.venv/bin/uvicorn zai_coder.production_hardening_core.server.asgi:app --host {config.host} --port {config.port} --proxy-headers
Restart=on-failure
RestartSec=5
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=full
ProtectHome=true
ReadWritePaths={config.install_dir}/data {config.install_dir}/logs {config.install_dir}/storage {config.install_dir}/backups

[Install]
WantedBy=multi-user.target
"""


def systemd_install_plan(config: DeployInstallConfig | None = None) -> dict:
    config = config or DeployInstallConfig()
    unit_path = f"/etc/systemd/system/{config.app_name}.service"
    return {
        "dry_run": True,
        "unit_path": unit_path,
        "commands": [
            f"sudo cp deploy/templates/{config.app_name}.service {unit_path}",
            "sudo systemctl daemon-reload",
            f"sudo systemctl enable {config.app_name}.service",
            f"sudo systemctl start {config.app_name}.service",
            f"sudo systemctl status {config.app_name}.service --no-pager",
        ],
    }
