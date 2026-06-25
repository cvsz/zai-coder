"""Notification draft adapters."""

from __future__ import annotations

import json

from zai_coder.integration_core.models import IntegrationPlan


def email_draft(to: str, subject: str, body: str) -> IntegrationPlan:
    return IntegrationPlan(
        provider="notifications",
        action="email_draft",
        payload={"to": to, "subject": subject, "body": body},
        warnings=["Draft only. No email was sent."],
    )


def slack_payload_draft(channel: str, text: str) -> IntegrationPlan:
    return IntegrationPlan(
        provider="notifications",
        action="slack_payload",
        payload={"channel": channel, "text": text},
        files={"slack-payload.json": json.dumps({"channel": channel, "text": text}, indent=2)},
        warnings=["Payload only. No Slack webhook was called."],
    )


def discord_payload_draft(content: str) -> IntegrationPlan:
    return IntegrationPlan(
        provider="notifications",
        action="discord_payload",
        payload={"content": content},
        files={"discord-payload.json": json.dumps({"content": content}, indent=2)},
        warnings=["Payload only. No Discord webhook was called."],
    )


def telegram_payload_draft(chat_id: str, text: str) -> IntegrationPlan:
    return IntegrationPlan(
        provider="notifications",
        action="telegram_payload",
        payload={"chat_id": chat_id, "text": text},
        files={"telegram-payload.json": json.dumps({"chat_id": chat_id, "text": text}, indent=2)},
        warnings=["Payload only. No Telegram API was called."],
    )
