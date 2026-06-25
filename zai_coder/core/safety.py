from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path


@dataclass
class SafetyResult:
    allowed: bool
    reason: str = ""


class SafetyPolicy:
    def __init__(self, allow_apps_zlms: bool = False):
        self.allow_apps_zlms = allow_apps_zlms
        self.block_patterns: list[tuple[re.Pattern[str], str]] = [
            (re.compile(r"\bgit\s+add\s+\.(?:$|\s)"), "Blocked: use exact-path staging, not git add ."),
            (re.compile(r"\bgit\s+add\s+-A(?:$|\s)"), "Blocked: use exact-path staging, not git add -A"),
            (re.compile(r"--no-verify\b"), "Blocked: --no-verify bypasses checks"),
            (re.compile(r"\bgit\s+push\b.*\s(-f|--force|--force-with-lease)\b"), "Blocked: force push is disabled"),
            (re.compile(r"\brm\s+-rf\s+(/|~|\$HOME|\.)($|\s)"), "Blocked: broad rm -rf is dangerous"),
            (re.compile(r"\bsudo\s+rm\s+-rf\b"), "Blocked: sudo rm -rf requires manual review"),
            (re.compile(r"\bchmod\s+-R\s+777\b"), "Blocked: recursive chmod 777 is unsafe"),
        ]
        self.generated_paths = [
            "node_modules/", "dist/", ".next/", "coverage/", "reports/", ".turbo/", ".vite/", "vendor/ai-assets/"
        ]

    def check_command(self, command: str) -> SafetyResult:
        normalized = command.strip()
        for pattern, reason in self.block_patterns:
            if pattern.search(normalized):
                return SafetyResult(False, reason)
        if not self.allow_apps_zlms and "apps/zlms/" in normalized:
            return SafetyResult(False, "Blocked: apps/zlms/** is protected by default")
        return SafetyResult(True, "OK")

    def check_path(self, path: str) -> SafetyResult:
        p = path.replace("\\", "/")
        if not self.allow_apps_zlms and p.startswith("apps/zlms/"):
            return SafetyResult(False, "Blocked path: apps/zlms/**")
        for generated in self.generated_paths:
            if generated in p or p.startswith(generated):
                return SafetyResult(False, f"Blocked generated path: {generated}")
        if ".env" in Path(p).name or "secret" in p.lower() or "token" in p.lower():
            return SafetyResult(False, "Blocked possible secret file")
        return SafetyResult(True, "OK")
