"""Approved command runner.

The runner is dry-run-first and uses subprocess without shell=True. It blocks
dangerous commands and requires an approval id before apply execution.
"""

from __future__ import annotations

import os
import subprocess
import uuid

from .models import CommandSpec, ExecutionResult, QueueItem, now_iso
from .safety import command_safety_report, approval_report
from .timeout_policy import TimeoutPolicy
from .journal import ExecutionJournal


class ApprovedCommandRunner:
    def __init__(self, journal: ExecutionJournal | None = None, timeout_policy: TimeoutPolicy | None = None):
        self.journal = journal or ExecutionJournal()
        self.timeout_policy = timeout_policy or TimeoutPolicy()

    def run_item(self, item: QueueItem) -> ExecutionResult:
        result = self.run_command(item.command, item.id)
        self.journal.record(item, result)
        return result

    def run_command(self, spec: CommandSpec, execution_id: str | None = None) -> ExecutionResult:
        execution_id = execution_id or str(uuid.uuid4())
        started = now_iso()
        safety = command_safety_report(spec.command, spec.cwd)
        approval = approval_report(spec.apply, spec.approval_id)
        blocked = tuple(safety["issues"] + ([] if approval["ok"] else [approval["reason"]]))
        if blocked:
            return ExecutionResult(
                id=execution_id,
                ok=False,
                status="blocked",
                returncode=None,
                stdout="",
                stderr="",
                dry_run=not spec.apply,
                started_at=started,
                finished_at=now_iso(),
                blocked_reasons=blocked,
            )
        if not spec.apply:
            return ExecutionResult(
                id=execution_id,
                ok=True,
                status="planned",
                returncode=None,
                stdout="DRY-RUN: " + " ".join(spec.command),
                stderr="",
                dry_run=True,
                started_at=started,
                finished_at=now_iso(),
            )

        env = os.environ.copy()
        env.update(spec.env_overlay)
        try:
            completed = subprocess.run(
                list(spec.command),
                cwd=spec.cwd,
                env=env,
                capture_output=True,
                text=True,
                timeout=self.timeout_policy.normalize(spec.timeout_seconds),
                check=False,
            )
            status = "completed" if completed.returncode == 0 else "failed"
            return ExecutionResult(
                id=execution_id,
                ok=completed.returncode == 0,
                status=status,
                returncode=completed.returncode,
                stdout=completed.stdout[-10000:],
                stderr=completed.stderr[-10000:],
                dry_run=False,
                started_at=started,
                finished_at=now_iso(),
            )
        except subprocess.TimeoutExpired as exc:
            return ExecutionResult(
                id=execution_id,
                ok=False,
                status="timeout",
                returncode=None,
                stdout=(exc.stdout or "")[-10000:] if isinstance(exc.stdout, str) else "",
                stderr=(exc.stderr or "")[-10000:] if isinstance(exc.stderr, str) else "",
                dry_run=False,
                started_at=started,
                finished_at=now_iso(),
                blocked_reasons=("timeout",),
            )
