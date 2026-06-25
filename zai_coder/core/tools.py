from __future__ import annotations

import os
import subprocess
from dataclasses import dataclass
from pathlib import Path

from .safety import SafetyPolicy


@dataclass
class ToolResult:
    ok: bool
    stdout: str = ""
    stderr: str = ""
    exit_code: int = 0
    blocked_reason: str = ""


class ToolRuntime:
    def __init__(self, workspace: str = ".", safety: SafetyPolicy | None = None, timeout: int = 180):
        self.workspace = Path(workspace).expanduser().resolve()
        self.safety = safety or SafetyPolicy()
        self.timeout = timeout

    def run(self, command: str) -> ToolResult:
        check = self.safety.check_command(command)
        if not check.allowed:
            return ToolResult(ok=False, blocked_reason=check.reason, exit_code=126)
        try:
            proc = subprocess.run(
                command,
                cwd=str(self.workspace),
                shell=True,
                text=True,
                capture_output=True,
                timeout=self.timeout,
            )
            return ToolResult(ok=proc.returncode == 0, stdout=proc.stdout, stderr=proc.stderr, exit_code=proc.returncode)
        except subprocess.TimeoutExpired as exc:
            return ToolResult(ok=False, stdout=exc.stdout or "", stderr=exc.stderr or "timeout", exit_code=124)

    def read_file(self, path: str, max_chars: int = 100_000) -> ToolResult:
        check = self.safety.check_path(path)
        if not check.allowed:
            return ToolResult(ok=False, blocked_reason=check.reason, exit_code=126)
        target = (self.workspace / path).resolve()
        if not str(target).startswith(str(self.workspace)):
            return ToolResult(ok=False, blocked_reason="Path escapes workspace", exit_code=126)
        try:
            return ToolResult(ok=True, stdout=target.read_text(encoding="utf-8", errors="replace")[:max_chars])
        except Exception as exc:  # noqa: BLE001
            return ToolResult(ok=False, stderr=str(exc), exit_code=1)

    def write_file(self, path: str, content: str) -> ToolResult:
        check = self.safety.check_path(path)
        if not check.allowed:
            return ToolResult(ok=False, blocked_reason=check.reason, exit_code=126)
        target = (self.workspace / path).resolve()
        if not str(target).startswith(str(self.workspace)):
            return ToolResult(ok=False, blocked_reason="Path escapes workspace", exit_code=126)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        return ToolResult(ok=True, stdout=f"wrote {target}\n")
