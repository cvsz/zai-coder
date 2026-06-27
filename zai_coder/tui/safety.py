from __future__ import annotations

import re

ALLOWED_TUI_COMMANDS = {
    ("./run.sh", "doctor"),
    ("make", "safety-check"),
    ("make", "repo-check"),
    ("make", "secret-scan"),
    ("make", "final-release-status"),
    ("make", "install-dry-run"),
    ("python3", "-m", "pytest", "-q"),
    ("python3", "-m", "compileall", "-q", "zai_coder"),
    ("./run.sh", "tui", "--print-config"),
}

FORBIDDEN_PATTERNS = [
    r"\bgit\s+add\s+(\.|-A)(\s|$)",
    r"\bgit\s+commit\b.*\s--no-verify\b",
    r"\bgit\s+push\b",
    r"\bgit\s+push\b.*\s--force\b",
    r"\brm\s+-rf\b",
    r"\bgh\s+release\b",
    r"\bterraform\s+apply\b",
    r"\bkubectl\s+apply\b",
    r"\bdocker\s+push\b",
    r"\bcloudflare\b",
    r"\bstripe\b",
    r"(^|\s)APPLY=1(\s|$)",
    r"\b(curl|wget)\b.*\b(https?://|ftp://)",
    r"\b(curl|wget)\b.*\|\s*bash\b",
]

SECRET_COMMAND_PATTERNS = [
    r"\bapi[_-]?key\s*[:=]",
    r"\baccess[_-]?token\s*[:=]",
    r"\bauth[_-]?token\s*[:=]",
    r"\bsecret\s*[:=]",
    r"\bcredential\s*[:=]",
    r"\bpassword\s*[:=]",
    r"\bprivate[_-]?key\s*[:=]",
    r"-----BEGIN\s+(RSA\s+|OPENSSH\s+|EC\s+)?PRIVATE\s+KEY-----",
]

def is_mutating_command(command: list[str]) -> bool:
    cmd_str = " ".join(str(part) for part in command)
    for pattern in FORBIDDEN_PATTERNS:
        if re.search(pattern, cmd_str, re.IGNORECASE):
            return True
    if contains_secret_like_text(cmd_str):
        return True
    return False

def require_dry_run_first(action_name: str, apply: bool, dry_run_completed: bool) -> bool:
    if not apply:
        return True
    return dry_run_completed

def redact_secret_text(text: str) -> str:
    redacted = text
    redacted = re.sub(
        r"(?i)(api[_-]?key|access[_-]?token|auth[_-]?token|token|password|secret|credential|private[_-]?key)\s*[:=]\s*(['\"]?)[^\s'\"}]+",
        r"\1=\2REDACTED",
        redacted,
    )
    redacted = re.sub(r"(?i)\b(sk|pk|ghp|github_pat|xoxb)-[A-Za-z0-9_\-]{8,}", r"\1-REDACTED", redacted)
    redacted = re.sub(
        r"-----BEGIN (RSA |OPENSSH |EC )?PRIVATE KEY-----.*?-----END (RSA |OPENSSH |EC )?PRIVATE KEY-----",
        "[REDACTED PRIVATE KEY BLOCK]",
        redacted,
        flags=re.DOTALL,
    )
    return redacted

def assert_allowed_tui_command(command: list[str]) -> None:
    if is_mutating_command(command):
        raise ValueError(f"Forbidden or secret-bearing TUI command blocked: {' '.join(command)}")
    command_tuple = tuple(command)
    if command_tuple not in ALLOWED_TUI_COMMANDS:
        allowed = ", ".join(" ".join(item) for item in sorted(ALLOWED_TUI_COMMANDS))
        raise ValueError(f"TUI command is not registered as local-safe: {' '.join(command)}. Allowed: {allowed}")


def contains_secret_like_text(text: str) -> bool:
    return _contains_secret_reference(text)


def _contains_secret_reference(value: str) -> bool:
    return any(re.search(pattern, value, re.IGNORECASE) for pattern in SECRET_COMMAND_PATTERNS)
