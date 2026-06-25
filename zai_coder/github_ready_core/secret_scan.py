from __future__ import annotations

import re
from pathlib import Path

PATTERNS = {
    "private_key": re.compile(r"-----BEGIN (RSA |EC |OPENSSH |)PRIVATE KEY-----"),
    "generic_secret_assignment": re.compile(r"(?i)(api[_-]?key|secret|token|password)\s*=\s*['\"]?[A-Za-z0-9_\-]{16,}"),
    "github_token": re.compile(r"gh[pousr]_[A-Za-z0-9_]{20,}"),
}
SKIP_DIRS = {".git", "__pycache__", ".pytest_cache", "node_modules", "dist", ".next", "coverage", "reports", "release"}
TEXT_SUFFIXES = {".py", ".md", ".txt", ".json", ".yml", ".yaml", ".sh", ".toml", ".ini", ".cfg", ""}

def scan_text(text: str) -> list[dict]:
    findings = []
    for name, pattern in PATTERNS.items():
        for match in pattern.finditer(text):
            findings.append({"type": name, "start": match.start(), "end": match.end()})
    return findings

def scan_repo(root: str | Path) -> dict:
    root = Path(root)
    findings = []
    for path in root.rglob("*"):
        rel = path.relative_to(root)
        rels = str(rel)
        if any(part in SKIP_DIRS for part in rel.parts) or rels.startswith(("docs/", "tests/")):
            continue
        if not path.is_file() or path.suffix not in TEXT_SUFFIXES:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for finding in scan_text(text):
            finding["path"] = rels
            findings.append(finding)
    return {"ok": not findings, "findings": findings}
