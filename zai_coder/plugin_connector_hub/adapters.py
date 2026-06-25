"""Connector adapter stubs.

Adapters return plans only. They do not call external APIs.
"""

from __future__ import annotations

from .catalog import find_connector


def connector_status_plan(connector_id: str) -> dict:
    connector = find_connector(connector_id)
    return {
        "dry_run": True,
        "connector": connector.to_dict(),
        "steps": [
            "validate manifest",
            "validate tenant permissions",
            "validate required env",
            "prepare status request",
            "record connector audit event",
        ],
    }


def connector_action_plan(connector_id: str, action: str, payload: dict | None = None) -> dict:
    connector = find_connector(connector_id)
    if action not in connector.supported_actions:
        raise ValueError(f"unsupported action for {connector_id}: {action}")
    return {
        "dry_run": True,
        "connector_id": connector_id,
        "action": action,
        "payload": payload or {},
        "steps": [
            f"prepare {action}",
            "validate no secrets in payload",
            "map request to provider adapter",
            "return plan only",
            "write audit event",
        ],
    }


def github_repo_plan(repo: str = "cvsz/zeaz-platform") -> dict:
    return connector_action_plan("github", "repo-plan", {"repo": repo})


def google_drive_index_plan(folder: str = "root") -> dict:
    return connector_action_plan("google-drive", "file-index-plan", {"folder": folder})


def slack_summary_plan(channel: str = "general") -> dict:
    return connector_action_plan("slack", "channel-summary-plan", {"channel": channel})


def cloudflare_access_plan(hostname: str = "zai.example.com") -> dict:
    return connector_action_plan("cloudflare", "access-plan", {"hostname": hostname})
