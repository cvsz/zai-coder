"""Connector catalog."""

from __future__ import annotations

from .models import ConnectorManifest


DEFAULT_CONNECTORS = [
    ConnectorManifest(
        id="github",
        name="GitHub",
        provider="github",
        version="1.0.0",
        description="Repository, PR, issue, and release planning connector.",
        category="developer",
        required_env=("GITHUB_TOKEN",),
        required_permissions=("connector:view", "connector:install", "github:read"),
        supported_actions=("status", "repo-plan", "issue-sync", "release-plan"),
        webhook_supported=True,
    ),
    ConnectorManifest(
        id="google-drive",
        name="Google Drive",
        provider="google_drive",
        version="1.0.0",
        description="Docs, Sheets, Slides, and file planning connector.",
        category="workspace",
        required_env=("GOOGLE_DRIVE_CLIENT_ID",),
        required_permissions=("connector:view", "connector:install", "drive:read"),
        supported_actions=("status", "file-index-plan", "doc-export-plan"),
        webhook_supported=False,
    ),
    ConnectorManifest(
        id="slack",
        name="Slack",
        provider="slack",
        version="1.0.0",
        description="Team notification and channel summary planning connector.",
        category="communications",
        required_env=("SLACK_BOT_TOKEN",),
        required_permissions=("connector:view", "connector:install", "slack:read"),
        supported_actions=("status", "channel-summary-plan", "notification-plan"),
        webhook_supported=True,
    ),
    ConnectorManifest(
        id="cloudflare",
        name="Cloudflare",
        provider="cloudflare",
        version="1.0.0",
        description="Cloudflare Access, DNS, tunnel, and go-live planning connector.",
        category="infrastructure",
        required_env=("CLOUDFLARE_API_TOKEN",),
        required_permissions=("connector:view", "connector:install", "providers:plan"),
        supported_actions=("status", "access-plan", "dns-plan", "tunnel-plan"),
        webhook_supported=False,
    ),
]


def connector_catalog() -> list[dict]:
    return [connector.to_dict() for connector in DEFAULT_CONNECTORS]


def find_connector(connector_id: str) -> ConnectorManifest:
    for connector in DEFAULT_CONNECTORS:
        if connector.id == connector_id:
            return connector
    raise ValueError(f"unknown connector: {connector_id}")


def search_connectors(query: str = "") -> dict:
    q = query.lower().strip()
    connectors = [
        c.to_dict()
        for c in DEFAULT_CONNECTORS
        if not q or q in c.name.lower() or q in c.description.lower() or q in c.category.lower() or q in " ".join(c.supported_actions).lower()
    ]
    return {"query": query, "connectors": connectors}
