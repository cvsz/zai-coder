"""Notification schedule planning."""

from __future__ import annotations


def schedule_notification_plan(draft_payload: dict, when: str = "next_business_day") -> dict:
    return {
        "dry_run": True,
        "draft_id": draft_payload["id"],
        "when": when,
        "scheduled": False,
        "send": False,
        "steps": [
            "validate preference",
            "render draft",
            "store in portal inbox",
            "review delivery gate",
            "manual approval if external delivery is ever added",
        ],
    }


def communication_calendar_policy() -> dict:
    return {
        "quiet_hours_respected": True,
        "max_customer_notices_per_day": 3,
        "digest_preferred_for_non_urgent": True,
        "no_external_calendar_write": True,
    }
