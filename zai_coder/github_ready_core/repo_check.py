from __future__ import annotations

from pathlib import Path

REQUIRED_FILES = [
    "README.md", "LICENSE", "CONTRIBUTING.md", "SECURITY.md", "CODE_OF_CONDUCT.md",
    "SUPPORT.md", "CHANGELOG.md", "ROADMAP.md", "RELEASE.md",
    ".github/workflows/ci.yml", ".github/PULL_REQUEST_TEMPLATE.md",
    ".gitignore", ".gitattributes", ".editorconfig",
]

DANGEROUS_PREFIXES = [
    "git add .",
    "git add -A",
    "git push --force",
    "docker system prune --volumes",
]

def _is_actionable_dangerous_line(line: str) -> bool:
    stripped = line.strip()
    if not stripped or stripped.startswith("#"):
        return False
    if stripped.startswith(("echo ", "print(", "assert ", "warnings", "FORBIDDEN_COMMANDS", "DANGEROUS_PREFIXES")):
        return False
    if "--no-verify" in stripped and stripped.startswith(("git commit", "git merge")):
        return True
    return any(stripped.startswith(prefix) for prefix in DANGEROUS_PREFIXES)

def check_required_files(root: str | Path) -> dict:
    root = Path(root)
    missing = [path for path in REQUIRED_FILES if not (root / path).exists()]
    return {"ok": not missing, "missing": missing}

def check_forbidden_commands(root: str | Path) -> dict:
    root = Path(root)
    findings = []
    scan_prefixes = ("scripts/", ".github/workflows/")
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(root)
        rels = str(rel)
        if not rels.startswith(scan_prefixes):
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        bad_lines = [line.strip() for line in text.splitlines() if _is_actionable_dangerous_line(line)]
        if bad_lines:
            findings.append({"path": rels, "forbidden": bad_lines})
    return {"ok": not findings, "findings": findings}

def repo_ready_report(root: str | Path) -> dict:
    required = check_required_files(root)
    forbidden = check_forbidden_commands(root)
    return {"ok": required["ok"] and forbidden["ok"], "required_files": required, "forbidden_commands": forbidden}
