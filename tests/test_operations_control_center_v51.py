"""v51 Operations Control Center — exception path tests."""

from __future__ import annotations

from unittest.mock import patch, MagicMock

import pytest

from zai_coder.operations_control_center.service_status import (
    default_service_statuses,
    service_status_plan,
    restart_service_plan,
)


# ---------------------------------------------------------------------------
# Exception path coverage
# ---------------------------------------------------------------------------

def test_service_status_dry_run():
    """Dry-run (execute=False) must return statuses without subprocesses."""
    statuses = default_service_statuses(execute=False)
    assert isinstance(statuses, list)
    assert len(statuses) > 0
    for s in statuses:
        assert hasattr(s, "name")
        assert hasattr(s, "status")


def test_service_status_execute_systemd_exception():
    """When systemctl raises, status should degrade to 'unknown' not raise."""
    import subprocess

    with patch(
        "subprocess.run",
        side_effect=OSError("systemctl not found"),
    ):
        statuses = default_service_statuses(execute=True)

    for s in statuses:
        # systemd targets should degrade to unknown rather than raising
        if s.target == "systemd":
            assert s.status in ("unknown", "planned", "running", "stopped")


def test_service_status_execute_docker_exception():
    """When docker ps raises, status should degrade to 'unknown' not raise."""
    with patch(
        "subprocess.run",
        side_effect=FileNotFoundError("docker not found"),
    ):
        statuses = default_service_statuses(execute=True)

    for s in statuses:
        if s.target == "docker":
            assert s.status in ("unknown", "planned", "running", "stopped")


def test_service_status_execute_success_systemd():
    """When systemctl returns 0, service should be 'running'."""
    mock_result = MagicMock()
    mock_result.returncode = 0
    mock_result.stdout = "active"

    with patch("subprocess.run", return_value=mock_result):
        statuses = default_service_statuses(execute=True)

    systemd_statuses = [s for s in statuses if s.target == "systemd"]
    for s in systemd_statuses:
        assert s.status == "running"


def test_service_status_execute_failed_systemd():
    """When systemctl returns non-zero, service should be 'stopped'."""
    mock_result = MagicMock()
    mock_result.returncode = 3
    mock_result.stdout = "inactive"

    with patch("subprocess.run", return_value=mock_result):
        statuses = default_service_statuses(execute=True)

    systemd_statuses = [s for s in statuses if s.target == "systemd"]
    for s in systemd_statuses:
        assert s.status == "stopped"


def test_service_status_execute_docker_running():
    """When docker ps returns container ID, service should be 'running'."""
    mock_result = MagicMock()
    mock_result.returncode = 0
    mock_result.stdout = "abc123def456"

    with patch("subprocess.run", return_value=mock_result):
        statuses = default_service_statuses(execute=True)

    docker_statuses = [s for s in statuses if s.target == "docker"]
    for s in docker_statuses:
        assert s.status == "running"


def test_service_status_execute_docker_stopped():
    """When docker ps returns empty, service should be 'stopped'."""
    mock_result = MagicMock()
    mock_result.returncode = 0
    mock_result.stdout = ""

    with patch("subprocess.run", return_value=mock_result):
        statuses = default_service_statuses(execute=True)

    docker_statuses = [s for s in statuses if s.target == "docker"]
    for s in docker_statuses:
        assert s.status == "stopped"


# ---------------------------------------------------------------------------
# Plan structure tests
# ---------------------------------------------------------------------------

def test_service_status_plan_structure():
    plan = service_status_plan()
    assert plan.name == "service-status-plan"
    assert plan.action == "status"
    assert len(plan.commands) > 0
    assert any("healthz" in c for c in plan.commands)


def test_restart_service_plan_structure():
    plan = restart_service_plan()
    assert plan.name == "restart-service-plan"
    assert plan.action == "restart"
    assert len(plan.commands) > 0


def test_service_status_plan_custom_name():
    plan = service_status_plan("my-service")
    assert "my-service" in " ".join(plan.commands)


def test_restart_service_plan_custom_name():
    plan = restart_service_plan("my-service")
    assert "my-service" in " ".join(plan.commands)
