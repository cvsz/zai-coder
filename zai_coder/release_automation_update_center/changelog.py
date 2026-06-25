"""Changelog generator."""

from __future__ import annotations


def changelog_from_items(version: str, items: list[str], previous_version: str = "") -> str:
    safe_items = [item.strip() for item in items if item.strip()]
    body = "\n".join(f"- {item}" for item in safe_items) or "- No changes listed."
    compare = f"\n\nPrevious: {previous_version}" if previous_version else ""
    return f"""# Changelog {version}

## Added / Changed

{body}{compare}

## Safety

- Dry-run release plan.
- Checksums required.
- Rollback plan required.
- Approval required before publishing.
"""


def default_changelog(version: str = "v29.0.0") -> str:
    return changelog_from_items(
        version,
        [
            "Release automation center",
            "Update manifest builder",
            "Dry-run update planner",
            "Rollback and migration gates",
            "GitHub release draft generator",
        ],
        "v28.0.0",
    )
