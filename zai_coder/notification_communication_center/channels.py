"""Notification channels and delivery policy."""

from __future__ import annotations


CHANNELS = [
    {"id": "portal", "name": "Portal Inbox", "external": False, "enabled": True},
    {"id": "in_app", "name": "In-App Banner", "external": False, "enabled": True},
    {"id": "email", "name": "Email Draft", "external": True, "enabled": False},
    {"id": "sms", "name": "SMS Draft", "external": True, "enabled": False},
    {"id": "slack", "name": "Slack Draft", "external": True, "enabled": False},
    {"id": "webhook", "name": "Webhook Draft", "external": True, "enabled": False},
]


def channel_catalog() -> list[dict]:
    return [dict(channel) for channel in CHANNELS]


def channel_policy(channel_id: str) -> dict:
    channel = next((item for item in CHANNELS if item["id"] == channel_id), None)
    if not channel:
        raise ValueError(f"unknown channel: {channel_id}")
    return {
        "channel": channel,
        "send_enabled": channel["enabled"] and not channel["external"],
        "external_delivery_disabled": channel["external"],
        "draft_only": True,
        "requires_review": True,
    }


def channel_validation_report() -> dict:
    ids = [channel["id"] for channel in CHANNELS]
    return {"ok": len(ids) == len(set(ids)), "channels": channel_catalog()}
