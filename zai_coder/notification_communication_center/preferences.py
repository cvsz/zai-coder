"""Notification preferences."""

from __future__ import annotations

from .models import NotificationPreference


DEFAULT_PREFERENCES = [
    NotificationPreference("pref-demo-portal", "cust_demo", "portal", True, "product", "immediate"),
    NotificationPreference("pref-demo-release", "cust_demo", "portal", True, "release", "weekly"),
    NotificationPreference("pref-demo-email", "cust_demo", "email", False, "product", "weekly"),
    NotificationPreference("pref-local-system", "cust_local", "in_app", True, "system", "immediate"),
]


def preference_catalog() -> list[dict]:
    return [pref.to_dict() for pref in DEFAULT_PREFERENCES]


def preference_validation_report() -> dict:
    reports = [{"id": pref.id, "issues": pref.validate()} for pref in DEFAULT_PREFERENCES]
    return {"ok": all(not item["issues"] for item in reports), "reports": reports}


def preference_decision(customer_id: str, channel: str, topic: str) -> dict:
    matches = [pref for pref in DEFAULT_PREFERENCES if pref.customer_id == customer_id and pref.channel == channel and pref.topic == topic]
    if not matches:
        return {"allowed": channel in {"portal", "in_app"}, "reason": "default local channel fallback", "frequency": "immediate"}
    pref = matches[0]
    return {"allowed": pref.enabled and pref.frequency != "never", "reason": "preference matched", "frequency": pref.frequency, "preference": pref.to_dict()}
