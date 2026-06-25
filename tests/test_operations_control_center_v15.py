from pathlib import Path

import pytest

from zai_coder.operations_control_center.models import ServiceStatus, OperationPlan, HealthSignal
from zai_coder.operations_control_center.service_status import default_service_statuses, service_status_plan, restart_service_plan
from zai_coder.operations_control_center.health_dashboard import default_health_signals, health_summary, render_health_dashboard
from zai_coder.operations_control_center.log_viewer import is_safe_log_path, tail_log, render_log_viewer
from zai_coder.operations_control_center.backup_dashboard import backup_action_plan, restore_action_plan, render_backup_dashboard
from zai_coder.operations_control_center.upgrade_dashboard import upgrade_action_plan, rollback_action_plan, render_upgrade_dashboard
from zai_coder.operations_control_center.ui.pages import render_ops_overview, render_services_page, render_health_page, render_backup_page, render_upgrade_page
from zai_coder.operations_control_center.routes import (
    route_ops_status,
    route_ops_overview,
    route_ops_services,
    route_ops_services_page,
    route_ops_health,
    route_ops_health_page,
    route_ops_logs,
    route_ops_logs_page,
    route_ops_backup,
    route_ops_restore,
    route_ops_upgrade,
    route_ops_upgrade_page,
    route_ops_rollback,
    route_ops_service_status_plan,
    route_ops_restart_plan,
)


def test_models_validate():
    assert ServiceStatus("svc", "local", "running").validate() == []
    assert ServiceStatus("", "bad", "bad").validate()
    assert OperationPlan("n", "a").to_dict()["dry_run"] is True
    assert HealthSignal("h", True).to_dict()["ok"] is True


def test_service_status_and_action_plans():
    statuses = default_service_statuses()
    assert any(s.target == "cloudflare" for s in statuses)
    assert service_status_plan().dry_run is True
    restart = restart_service_plan()
    assert restart.dry_run is True
    assert restart.requires_approval is True


def test_health_dashboard():
    signals = default_health_signals()
    summary = health_summary(signals)
    assert summary["ok"] is True
    html = render_health_dashboard(signals)
    assert "Health Dashboard" in html


def test_safe_log_viewer(tmp_path, monkeypatch):
    log_dir = tmp_path / "logs"
    log_dir.mkdir()
    log_file = log_dir / "zai-coder.log"
    log_file.write_text("a\\nb\\nc\\n", encoding="utf-8")
    monkeypatch.chdir(tmp_path)
    assert is_safe_log_path("logs/zai-coder.log")
    assert not is_safe_log_path("../secret")
    assert not is_safe_log_path("/etc/passwd")
    result = tail_log("logs/zai-coder.log", 2)
    assert result["lines"] == ["b", "c"]
    assert "Log Viewer" in render_log_viewer(result)


def test_backup_upgrade_dashboards():
    assert backup_action_plan()["dry_run"] is True
    assert restore_action_plan("backups/example.tar.gz")["dry_run"] is True
    assert "Backup Dashboard" in render_backup_dashboard()
    assert upgrade_action_plan("v0.15.0")["dry_run"] is True
    assert rollback_action_plan("v0.14.0")["dry_run"] is True
    assert "Upgrade Dashboard" in render_upgrade_dashboard()


def test_ui_pages_render():
    assert "Operations Control Center" in render_ops_overview()
    assert "Service Status" in render_services_page()
    assert "Health" in render_health_page()
    assert "Backup" in render_backup_page()
    assert "Upgrade" in render_upgrade_page()


def test_routes():
    assert route_ops_status()["ok"] is True
    assert route_ops_overview()["content_type"] == "text/html"
    assert "services" in route_ops_services()
    assert route_ops_services_page()["content_type"] == "text/html"
    assert "signals" in route_ops_health()
    assert route_ops_health_page()["content_type"] == "text/html"
    assert route_ops_logs()["exists"] is False
    assert route_ops_logs_page()["content_type"] == "text/html"
    assert route_ops_backup()["dry_run"] is True
    assert route_ops_restore("backups/example.tar.gz")["dry_run"] is True
    assert route_ops_upgrade("v0.15.0")["dry_run"] is True
    assert route_ops_upgrade_page("v0.15.0")["content_type"] == "text/html"
    assert route_ops_rollback("v0.14.0")["dry_run"] is True
    assert route_ops_service_status_plan()["dry_run"] is True
    assert route_ops_restart_plan()["dry_run"] is True


def test_docs_scripts_assets_exist():
    root = Path(__file__).resolve().parents[1]
    for rel in [
        "scripts/ops-center/status-panel.sh",
        "scripts/ops-center/health-dashboard.sh",
        "scripts/ops-center/log-viewer.sh",
        "scripts/ops-center/backup-dashboard.sh",
        "scripts/ops-center/upgrade-dashboard.sh",
        "scripts/ops-center/action-plans.sh",
        "docs/operations/OPS_CONTROL_CENTER.md",
        "docs/operations/SERVICE_STATUS_PANEL.md",
        "docs/operations/LOG_VIEWER.md",
        "docs/operations/UPGRADE_BACKUP_DASHBOARD.md",
        "docs/requirements/NEXT_V15_OPERATIONS_CONTROL_CENTER_REQUIREMENTS.md",
        "assets/ops-center/ops_control_center_features.json",
    ]:
        assert (root / rel).exists(), rel
