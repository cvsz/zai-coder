from pathlib import Path
import tempfile

from zai_coder.execution_runner.models import CommandSpec
from zai_coder.execution_runner.safety import command_safety_report, approval_report, is_safe_cwd
from zai_coder.execution_runner.timeout_policy import TimeoutPolicy
from zai_coder.execution_runner.retry_policy import ExecutionRetryPolicy
from zai_coder.execution_runner.queue import ExecutionQueue
from zai_coder.execution_runner.runner import ApprovedCommandRunner
from zai_coder.execution_runner.journal import ExecutionJournal
from zai_coder.execution_runner.rollback_hooks import list_rollback_hooks, rollback_hook_for
from zai_coder.execution_runner.recovery import failed_operation_recovery_plan
from zai_coder.execution_runner.approval_dashboard import render_approval_dashboard, approval_token_plan
from zai_coder.execution_runner.audit_timeline import render_execution_timeline
from zai_coder.execution_runner.routes import (
    route_execution_status,
    route_command_safety,
    route_enqueue,
    route_run_next,
    route_journal,
    route_rollback_hooks,
    route_rollback_hook,
    route_recovery_plan,
    route_approval_plan,
    route_approval_dashboard,
    route_execution_timeline,
    route_timeout_policy,
    route_retry_policy,
)


def test_safety_policy():
    assert command_safety_report(("echo", "hello"))["ok"] is True
    assert command_safety_report(("rm", "-rf", "/"))["ok"] is False
    assert command_safety_report(("git", "add", "."))["ok"] is False
    assert not is_safe_cwd("../x")
    assert approval_report(False, "")["ok"] is True
    assert approval_report(True, "")["ok"] is False
    assert approval_report(True, "approved_manual_001")["ok"] is True


def test_timeout_and_retry_policies():
    assert TimeoutPolicy().normalize(None) == 60
    assert TimeoutPolicy().normalize(9999) == 600
    retry = ExecutionRetryPolicy()
    assert retry.should_retry(1, "failed") is True
    assert retry.should_retry(3, "failed") is False
    assert retry.delay_for_attempt(2) == 6


def test_queue_journal_and_runner_dry_run():
    with tempfile.TemporaryDirectory() as td:
        q = ExecutionQueue(Path(td) / "queue.db")
        journal = ExecutionJournal(Path(td) / "journal.db")
        cmd = CommandSpec(command=("echo", "hello"), apply=False)
        item = q.enqueue("local", "demo", cmd)
        assert q.next_item().id == item.id
        result = ApprovedCommandRunner(journal).run_item(item)
        assert result.ok is True
        assert result.dry_run is True
        assert "DRY-RUN" in result.stdout
        events = journal.list_events()
        assert events and events[0]["id"] == result.id


def test_runner_blocks_unsafe_apply_and_can_apply_safe_echo():
    with tempfile.TemporaryDirectory() as td:
        journal = ExecutionJournal(Path(td) / "journal.db")
        runner = ApprovedCommandRunner(journal)
        blocked = runner.run_command(CommandSpec(command=("rm", "-rf", "/"), apply=True, approval_id="approved_manual_001"))
        assert blocked.ok is False
        assert blocked.status == "blocked"

        ok = runner.run_command(CommandSpec(command=("echo", "hello"), apply=True, approval_id="approved_manual_001", timeout_seconds=5))
        assert ok.ok is True
        assert ok.dry_run is False
        assert "hello" in ok.stdout


def test_rollback_recovery_approval_timeline():
    hooks = list_rollback_hooks()
    assert hooks
    assert rollback_hook_for("docker_compose_up") is not None
    recovery = failed_operation_recovery_plan("docker", "docker_compose_up")
    assert recovery["dry_run"] is True
    assert recovery["rollback_hook"] is not None
    assert "Human Approval Dashboard" in render_approval_dashboard([])
    assert approval_token_plan()["dry_run"] is True
    assert "Execution Audit Timeline" in render_execution_timeline([])


def test_routes(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    assert route_execution_status()["ok"] is True
    assert route_command_safety({"command": ["echo", "hello"]})["ok"] is True
    item = route_enqueue({"provider": "local", "action": "demo", "command": ["echo", "hello"]})
    assert item["status"] == "queued"
    ran = route_run_next()
    assert ran["ran"] is True
    assert "events" in route_journal()
    assert route_rollback_hooks()["hooks"]
    assert route_rollback_hook("docker_compose_up")["hook"] is not None
    assert route_recovery_plan("docker", "docker_compose_up")["dry_run"] is True
    assert route_approval_plan()["dry_run"] is True
    assert route_approval_dashboard()["content_type"] == "text/html"
    assert route_execution_timeline()["content_type"] == "text/html"
    assert route_timeout_policy()["default_seconds"] == 60
    assert route_retry_policy()["max_attempts"] == 3


def test_docs_scripts_assets_exist():
    root = Path(__file__).resolve().parents[1]
    for rel in [
        "scripts/execution/execution-status.sh",
        "scripts/execution/command-safety.sh",
        "scripts/execution/enqueue-demo.sh",
        "scripts/execution/run-next.sh",
        "scripts/execution/journal.sh",
        "scripts/execution/rollback-hooks.sh",
        "scripts/execution/recovery-plan.sh",
        "scripts/execution/approval-plan.sh",
        "scripts/execution/timeline-export.sh",
        "docs/execution/EXECUTION_RUNNER_GUIDE.md",
        "docs/execution/COMMAND_SAFETY_POLICY.md",
        "docs/execution/RECOVERY_AND_ROLLBACK.md",
        "docs/requirements/NEXT_V18_EXECUTION_RUNNER_REQUIREMENTS.md",
        "assets/execution/execution_runner_features.json",
    ]:
        assert (root / rel).exists(), rel
