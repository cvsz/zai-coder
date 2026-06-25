"""GitHub integration adapter."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

from zai_coder.integration_core.models import IntegrationPlan


BLOCKED_PATH_PARTS = {".env", "node_modules", "dist", ".next", "coverage", "reports", "__pycache__", ".pytest_cache"}


def is_safe_repo_path(path: str) -> bool:
    p = Path(path)
    normalized = str(path).replace("\\", "/")
    if p.is_absolute() or ".." in p.parts:
        return False
    if normalized.startswith("apps/zlms/"):
        return False
    if any(part in p.parts for part in BLOCKED_PATH_PARTS):
        return False
    return True


def repo_status_plan(repo: str = ".") -> IntegrationPlan:
    return IntegrationPlan(
        provider="github",
        action="repo_status",
        commands=["git status --short", "git branch --show-current", "gh auth status"],
        payload={"repo": repo},
    )


def exact_path_publish_plan(paths: Iterable[str], branch: str = "main") -> IntegrationPlan:
    safe_paths = []
    blocked = []
    for path in paths:
        if is_safe_repo_path(path):
            safe_paths.append(path)
        else:
            blocked.append(path)

    commands = [f"git add -- {path}" for path in safe_paths]
    commands.extend([
        "git status --short",
        'git commit -S -m "chore: publish exact-path update"',
        f"git push -u origin {branch}",
    ])

    warnings = ["blocked unsafe paths: " + ", ".join(blocked)] if blocked else []
    warnings.append("Review before executing. Never replace this with git add . or git add -A.")

    return IntegrationPlan(
        provider="github",
        action="exact_path_publish_plan",
        commands=commands,
        payload={"branch": branch, "safe_paths": safe_paths, "blocked_paths": blocked},
        warnings=warnings,
    )


def pr_summary_plan(pr_number: int, repo_full_name: str) -> IntegrationPlan:
    return IntegrationPlan(
        provider="github",
        action="pr_summary",
        commands=[f"gh pr view {pr_number} --repo {repo_full_name} --json title,body,files,commits,reviews"],
        payload={"repo_full_name": repo_full_name, "pr_number": pr_number},
    )


def release_draft_plan(version: str, title: str = "") -> IntegrationPlan:
    title = title or f"ZAI Coder {version}"
    return IntegrationPlan(
        provider="github",
        action="release_draft",
        commands=[f'gh release create {version} --draft --title "{title}" --notes-file docs/github/GITHUB_RELEASE_PROCESS.md'],
        payload={"version": version, "title": title},
        warnings=["Draft release only. Review notes and artifacts before publishing."],
    )
