from __future__ import annotations

from pathlib import Path

FORBIDDEN_COMMANDS = ["git add .", "git add -A", "--no-verify", "push --force", "docker system prune --volumes"]
BLOCKED_PATH_PREFIXES = ["apps/zlms/", "node_modules/", "dist/", ".next/", "coverage/", "reports/", "release/", "data/", "logs/", "backups/"]
BLOCKED_FILENAMES = {".env", "credentials.json", "creds.json", "secrets.json", "terraform.tfvars"}

def is_safe_stage_path(path: str) -> bool:
    p = Path(path)
    normalized = str(path).replace("\\", "/")
    if not normalized or p.is_absolute() or ".." in p.parts:
        return False
    if any(normalized.startswith(prefix) for prefix in BLOCKED_PATH_PREFIXES):
        return False
    if p.name in BLOCKED_FILENAMES or p.name.startswith(".env"):
        return False
    if p.suffix in {".pem", ".key", ".p12", ".pfx", ".tfstate"}:
        return False
    return True

def find_forbidden_command_text(text: str) -> list[str]:
    return [cmd for cmd in FORBIDDEN_COMMANDS if cmd in text]
