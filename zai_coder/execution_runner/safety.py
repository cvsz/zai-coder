"""Execution safety policy."""

from __future__ import annotations

from pathlib import Path

SAFE_EXECUTABLES = {
    "python",
    "python3",
    "pytest",
    "make",
    "git",
    "gh",
    "cloudflared",
    "docker",
    "curl",
    "echo",
}

BLOCKED_TOKENS = {
    "rm",
    "mkfs",
    "dd",
    "shutdown",
    "reboot",
    "poweroff",
    "sudo",
    "su",
    "chmod",
    "chown",
    ":(){",
    ">|",
}

BLOCKED_SUBSTRINGS = (
    "git add .",
    "git add -A",
    "--no-verify",
    "push --force",
    "docker system prune",
    "rm -rf",
    "/etc/passwd",
    "/etc/shadow",
)


def is_safe_cwd(cwd: str) -> bool:
    path = Path(cwd)
    if path.is_absolute() or ".." in path.parts:
        return False
    normalized = str(path).replace("\\", "/")
    return not normalized.startswith(("apps/zlms", ".git", "node_modules", "release", "backups"))


def command_safety_report(command: tuple[str, ...], cwd: str = ".") -> dict:
    issues: list[str] = []
    if not command:
        issues.append("empty command")
        return {"ok": False, "issues": issues}

    executable = command[0]
    joined = " ".join(command)
    if executable not in SAFE_EXECUTABLES:
        issues.append(f"executable not allowed: {executable}")
    if executable in BLOCKED_TOKENS:
        issues.append(f"blocked executable: {executable}")
    for token in command:
        if token in BLOCKED_TOKENS:
            issues.append(f"blocked token: {token}")
    for pattern in BLOCKED_SUBSTRINGS:
        if pattern in joined:
            issues.append(f"blocked pattern: {pattern}")
    if not is_safe_cwd(cwd):
        issues.append(f"unsafe cwd: {cwd}")
    return {"ok": not issues, "issues": issues, "command": list(command), "cwd": cwd}


def approval_report(apply: bool, approval_id: str) -> dict:
    if not apply:
        return {"ok": True, "reason": "dry-run"}
    if approval_id.startswith("approved_") and len(approval_id) >= 16:
        return {"ok": True, "reason": "approved"}
    return {"ok": False, "reason": "apply requires approval_id starting with approved_"}
