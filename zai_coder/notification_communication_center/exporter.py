"""Notification center exports."""

from __future__ import annotations

import json
from pathlib import Path

from .channels import channel_catalog, channel_validation_report
from .templates import notification_template_registry, notification_template_validation_report
from .preferences import preference_catalog, preference_validation_report
from .render import render_demo_notification
from .delivery import delivery_gate
from .scheduler import communication_calendar_policy


def notification_export_bundle() -> dict:
    demo = render_demo_notification()
    return {
        "kind": "zai-notification-communication-export",
        "version": "1.0",
        "channels": channel_catalog(),
        "channel_validation": channel_validation_report(),
        "templates": notification_template_registry(),
        "template_validation": notification_template_validation_report(),
        "preferences": preference_catalog(),
        "preference_validation": preference_validation_report(),
        "demo_draft": demo["draft"],
        "delivery_gate": delivery_gate(demo["draft"]),
        "calendar_policy": communication_calendar_policy(),
        "external_send": False,
        "requires_review": True,
    }


def write_notification_export(root: str | Path = ".", out: str = "notifications/exports/notification-center-export.json") -> str:
    root = Path(root)
    path = root / out
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(notification_export_bundle(), indent=2, sort_keys=True), encoding="utf-8")
    return str(path)


def write_notification_report(root: str | Path = ".", out: str = "notifications/reports/notification-center-report.md") -> str:
    bundle = notification_export_bundle()
    root = Path(root)
    path = root / out
    path.parent.mkdir(parents=True, exist_ok=True)
    channels = "\n".join(f"- {item['id']}: enabled={item['enabled']} external={item['external']}" for item in bundle["channels"])
    templates = "\n".join(f"- {item['title']} [{item['channel']}]" for item in bundle["templates"])
    path.write_text(f"""# Notification and Communication Center Report

## Channels

{channels}

## Templates

{templates}

## Safety

- Local portal/in-app drafts only.
- External sending is disabled.
- Delivery requires review.
- Demo writes require APPLY=1.
""", encoding="utf-8")
    return str(path)
