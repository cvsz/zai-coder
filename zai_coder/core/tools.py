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


from zai_coder.core.redaction import redact_text
from zai_coder.core.audit import AuditLog
from zai_coder.core.command_parser import CommandParser, CommandParseError
from zai_coder.core.command_profiles import get_allowed_commands

class ToolRuntime:
    def __init__(self, workspace: str = ".", safety: SafetyPolicy | None = None, timeout: int = 180, profile: str = "operator"):
        self.workspace = Path(workspace).expanduser().resolve()
        self.safety = safety or SafetyPolicy()
        self.timeout = timeout
        self.profile = profile
        self.audit = AuditLog(self.workspace / "data" / "zai-audit.jsonl")
        self.max_output_size = 1024 * 1024 # 1MB
        self.parser = CommandParser(str(self.workspace), timeout=self.timeout, env={"PATH": os.environ.get("PATH", ""), "HOME": os.environ.get("HOME", "")})

    def is_allowlisted(self, name: str) -> bool:
        return name in get_allowed_commands(self.profile)

    def run(self, command: str, allow_shell: bool = False) -> ToolResult:
        check = self.safety.check_command(command)
        if not check.allowed:
            self.audit.write("run_command", False, "Blocked by safety policy", command=command, reason=check.reason)
            return ToolResult(ok=False, blocked_reason=check.reason, exit_code=126)
            
        try:
            ctx = self.parser.parse(command)
        except CommandParseError as e:
            self.audit.write("run_command", False, "Parse error", command=command, reason=str(e))
            return ToolResult(ok=False, blocked_reason=f"Parse error: {e}", exit_code=126)

        if not allow_shell and not self.is_allowlisted(ctx["name"]):
            reason = f"Command {ctx['name']} not in allowlist for profile {self.profile}"
            self.audit.write("run_command", False, reason, command=command)
            return ToolResult(ok=False, blocked_reason=reason, exit_code=126)

        try:
            proc = subprocess.run(
                command if allow_shell else ctx["args"],
                cwd=ctx["cwd"],
                shell=allow_shell,
                text=True,
                capture_output=True,
                timeout=ctx["timeout"],
                env=ctx["env"] if not allow_shell else None
            )
            
            stdout = redact_text(proc.stdout)[:self.max_output_size]
            stderr = redact_text(proc.stderr)[:self.max_output_size]
            
            self.audit.write("run_command", proc.returncode == 0, "Executed command", command=command, exit_code=proc.returncode)
            return ToolResult(ok=proc.returncode == 0, stdout=stdout, stderr=stderr, exit_code=proc.returncode)
        except subprocess.TimeoutExpired as exc:
            stdout = redact_text(exc.stdout.decode('utf-8') if isinstance(exc.stdout, bytes) else (exc.stdout or ""))[:self.max_output_size]
            stderr = redact_text(exc.stderr.decode('utf-8') if isinstance(exc.stderr, bytes) else (exc.stderr or ""))[:self.max_output_size]
            self.audit.write("run_command", False, "Timeout", command=command)
            return ToolResult(ok=False, stdout=stdout, stderr=stderr, exit_code=124)
        except Exception as e:
            self.audit.write("run_command", False, "Exception", command=command, error=str(e))
            return ToolResult(ok=False, stderr=str(e), exit_code=1)

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
