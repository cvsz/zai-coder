from __future__ import annotations

import re
from pathlib import Path

PATTERNS = {
    "private_key": re.compile(r"-----BEGIN (RSA |EC |OPENSSH |)PRIVATE KEY-----"),
    "generic_secret_assignment": re.compile(r"(?i)(api[_-]?key|secret|token|password)\s*=\s*['\"]?[A-Za-z0-9_\-]{16,}"),
    "github_token": re.compile(r"gh[pousr]_[A-Za-z0-9_]{20,}"),
}
SKIP_DIRS = {".git", "__pycache__", ".pytest_cache", "node_modules", "dist", ".next", "coverage", "reports", "release"}
SKIP_FILES = {".env", ".env.local", ".env.development", ".env.production"}
TEXT_SUFFIXES = {".py", ".md", ".txt", ".json", ".yml", ".yaml", ".sh", ".toml", ".ini", ".cfg", ""}
PLACEHOLDER_MARKERS = (
    "change_me",
    "change-me",
    "replace-with",
    "placeholder",
    "example",
    "no-key-required",
    "token_preview",
)

def scan_text(text: str) -> list[dict]:
    findings = []
    for name, pattern in PATTERNS.items():
        for match in pattern.finditer(text):
            line_start = text.rfind("\n", 0, match.start()) + 1
            line_end = text.find("\n", match.end())
            matched_line = text[line_start : line_end if line_end != -1 else len(text)]
            context_start = max(0, line_start - 160)
            context_end = min(len(text), (line_end if line_end != -1 else len(text)) + 160)
            context = text[context_start:context_end].lower()
            if any(marker in context for marker in PLACEHOLDER_MARKERS):
                continue
            if name == "generic_secret_assignment":
                rhs = matched_line.split("=", 1)[1] if "=" in matched_line else ""
                if "(" in rhs or "." in rhs:
                    continue
            findings.append({"type": name, "start": match.start(), "end": match.end()})
    return findings

def scan_repo(root: str | Path) -> dict:
    root = Path(root)
    findings = []
    for path in root.rglob("*"):
        rel = path.relative_to(root)
        rels = str(rel)
        if path.name in SKIP_FILES:
            continue
        if any(part in SKIP_DIRS for part in rel.parts) or rels.startswith(("docs/", "tests/")):
            continue
        if not path.is_file() or path.suffix not in TEXT_SUFFIXES:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for finding in scan_text(text):
            finding["path"] = rels
            findings.append(finding)
    return {"ok": not findings, "findings": findings}
