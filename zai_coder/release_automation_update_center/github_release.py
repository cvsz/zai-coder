"""GitHub release draft generator.

No GitHub API call is made. This produces reviewable release text and a safe
manual command checklist.
"""

from __future__ import annotations

from .changelog import default_changelog


def github_release_draft(version: str = "v29.0.0", repo: str = "cvsz/zai-coder-control-plane") -> dict:
    return {
        "dry_run": True,
        "repo": repo,
        "tag": version,
        "title": f"ZAI Coder Control Plane {version}",
        "body": default_changelog(version),
        "manual_checks": [
            "confirm tests passed",
            "confirm repo-check passed",
            "confirm secret-scan passed",
            "confirm checksum manifest",
            "confirm rollback plan",
            "confirm approval id",
        ],
        "safe_git_policy": [
            "no force push",
            "no --no-verify",
            "no broad git add",
            "do not stage secrets or generated dependency folders",
        ],
    }


def github_release_command_plan(version: str = "v29.0.0") -> dict:
    return {
        "dry_run": True,
        "commands": [
            f"git tag -s {version} -m 'release: {version}'",
            f"gh release create {version} dist/*.zip --draft --title 'ZAI Coder Control Plane {version}' --notes-file RELEASE_NOTES.md",
        ],
        "requires_manual_review": True,
    }
