"""Operations Control Center route registry."""

from __future__ import annotations

from zai_coder.operations_control_center.service_status import default_service_statuses, service_status_plan, restart_service_plan
from zai_coder.operations_control_center.health_dashboard import health_summary, render_health_dashboard
from zai_coder.operations_control_center.log_viewer import tail_log, render_log_viewer
from zai_coder.operations_control_center.backup_dashboard import backup_action_plan, restore_action_plan, render_backup_dashboard
from zai_coder.operations_control_center.upgrade_dashboard import upgrade_action_plan, rollback_action_plan, render_upgrade_dashboard
from zai_coder.operations_control_center.ui.pages import render_ops_overview, render_services_page, render_health_page, render_backup_page, render_upgrade_page


def route_ops_status() -> dict:
    return {
        "ok": True,
        "service": "zai-operations-control-center",
        "systems": [
            "service_status_panel",
            "health_dashboard",
            "log_viewer",
            "backup_dashboard",
            "upgrade_dashboard",
            "rollback_dashboard",
            "operation_action_plans",
        ],
    }


def route_ops_overview() -> dict:
    return {"content_type": "text/html", "html": render_ops_overview()}


def route_ops_services() -> dict:
    return {"services": [service.to_dict() for service in default_service_statuses()]}


def route_ops_services_page() -> dict:
    return {"content_type": "text/html", "html": render_services_page()}


def route_ops_health() -> dict:
    return health_summary()


def route_ops_health_page() -> dict:
    return {"content_type": "text/html", "html": render_health_page()}


def route_ops_logs(path: str = "logs/zai-coder.log", lines: int = 100) -> dict:
    return tail_log(path, lines)


def route_ops_logs_page(path: str = "logs/zai-coder.log") -> dict:
    return {"content_type": "text/html", "html": render_log_viewer(tail_log(path))}


def route_ops_backup() -> dict:
    return backup_action_plan()


def route_ops_backup_page() -> dict:
    return {"content_type": "text/html", "html": render_backup_page()}


def route_ops_restore(archive: str) -> dict:
    return restore_action_plan(archive)


def route_ops_upgrade(version: str = "v0.15.0") -> dict:
    return upgrade_action_plan(version)


def route_ops_upgrade_page(version: str = "v0.15.0") -> dict:
    return {"content_type": "text/html", "html": render_upgrade_page()}


def route_ops_rollback(version: str = "v0.14.0") -> dict:
    return rollback_action_plan(version)


def route_ops_service_status_plan() -> dict:
    return service_status_plan().to_dict()


def route_ops_restart_plan() -> dict:
    return restart_service_plan().to_dict()
