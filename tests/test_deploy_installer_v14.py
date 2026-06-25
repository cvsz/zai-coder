from pathlib import Path

from zai_coder.deploy_installer_core.config import DeployInstallConfig, default_config
from zai_coder.deploy_installer_core.env_example import render_env_example
from zai_coder.deploy_installer_core.install_plan import ubuntu_install_plan, one_command_setup_plan
from zai_coder.deploy_installer_core.systemd import render_systemd_unit, systemd_install_plan
from zai_coder.deploy_installer_core.docker_launcher import docker_launch_plan
from zai_coder.deploy_installer_core.cloudflare import render_cloudflare_tunnel_config, cloudflare_plan
from zai_coder.deploy_installer_core.first_run import first_run_plan
from zai_coder.deploy_installer_core.healthcheck import healthcheck_plan
from zai_coder.deploy_installer_core.backup_restore import backup_plan, restore_plan
from zai_coder.deploy_installer_core.upgrade_rollback import upgrade_plan, rollback_plan
from zai_coder.deploy_installer_core.go_live import go_live_checklist


def test_config_defaults_and_validation():
    cfg = default_config()
    assert cfg.host == "127.0.0.1"
    assert cfg.port == 8765
    assert cfg.validate() == []
    bad = DeployInstallConfig(host="0.0.0.0")
    assert bad.validate()


def test_env_example():
    env = render_env_example()
    assert "ZAI_ENV=production" in env
    assert "DATABASE_URL=" in env
    assert "ZAI_SESSION_SECRET=" in env


def test_install_plans_are_dry_run():
    assert ubuntu_install_plan().dry_run is True
    assert one_command_setup_plan().dry_run is True
    assert "requirements-production.txt" in " ".join(ubuntu_install_plan().commands)


def test_systemd_and_docker_plans():
    unit = render_systemd_unit()
    assert "NoNewPrivileges=true" in unit
    assert "--host 127.0.0.1" in unit
    plan = systemd_install_plan()
    assert plan["dry_run"] is True
    docker = docker_launch_plan()
    assert docker["dry_run"] is True
    assert "docker compose" in docker["commands"][0]


def test_cloudflare_first_run_health():
    cfg = render_cloudflare_tunnel_config()
    assert "http://127.0.0.1:8765" in cfg
    plan = cloudflare_plan()
    assert plan["dry_run"] is True
    first = first_run_plan("admin@example.com")
    assert first["dry_run"] is True
    assert "verify /healthz" in first["steps"]
    health = healthcheck_plan()
    assert "/healthz" in health["commands"][0]


def test_backup_restore_upgrade_rollback_go_live():
    backup = backup_plan()
    assert backup["dry_run"] is True
    assert "apps/zlms" in backup["exclude"]
    restore = restore_plan("backups/example.tar.gz")
    assert restore["dry_run"] is True
    upgrade = upgrade_plan("v0.14.0")
    rollback = rollback_plan("v0.13.0")
    assert upgrade["dry_run"] is True
    assert rollback["dry_run"] is True
    checklist = go_live_checklist()
    assert any(item["area"] == "cloudflare" for item in checklist)
    assert all("required" in item for item in checklist)


def test_deploy_installer_files_exist():
    root = Path(__file__).resolve().parents[1]
    files = [
        "install.sh",
        ".env.example",
        "scripts/install/ubuntu-24-04-install.sh",
        "scripts/deploy/deploy-local.sh",
        "scripts/deploy/deploy-systemd-safe.sh",
        "scripts/deploy/deploy-docker-safe.sh",
        "scripts/deploy/cloudflare-plan.sh",
        "scripts/ops/healthcheck.sh",
        "scripts/ops/backup-safe.sh",
        "scripts/ops/restore-safe.sh",
        "scripts/ops/upgrade-safe.sh",
        "scripts/ops/rollback-safe.sh",
        "scripts/ops/go-live-checklist.sh",
        "docs/deploy/DEPLOY_INSTALLER_GUIDE.md",
        "docs/operations/GO_LIVE_CHECKLIST.md",
        "docs/operations/UPGRADE_ROLLBACK.md",
        "docs/operations/BACKUP_RESTORE_RUNBOOK.md",
        "docs/operations/HEALTHCHECK_RUNBOOK.md",
        "deploy/templates/zai-coder-control-plane.service",
    ]
    for rel in files:
        assert (root / rel).exists(), rel
