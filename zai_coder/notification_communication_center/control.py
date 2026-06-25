"""Notification and Communication Center control helpers."""

from __future__ import annotations

from .channels import channel_catalog, channel_validation_report, channel_policy
from .templates import notification_template_registry, notification_template_validation_report
from .preferences import preference_catalog, preference_validation_report
from .render import render_demo_notification
from .delivery import delivery_gate, digest_plan
from .inbox import PortalInbox, thread_from_drafts
from .scheduler import schedule_notification_plan, communication_calendar_policy
from .exporter import write_notification_export, write_notification_report, notification_export_bundle
from .audit import NotificationAuditLog


def notification_center_status() -> dict:
    return {
        "ok": True,
        "systems": [
            "channel_policy_registry",
            "notification_template_registry",
            "preference_center",
            "safe_draft_renderer",
            "delivery_gate",
            "portal_inbox",
            "digest_schedule_planner",
            "communication_thread_builder",
            "notification_exports",
            "notification_audit_log",
        ],
    }


def notification_center_overview() -> dict:
    demo = render_demo_notification()
    return {
        "status": notification_center_status(),
        "channels": channel_catalog(),
        "channel_validation": channel_validation_report(),
        "templates": notification_template_registry(),
        "template_validation": notification_template_validation_report(),
        "preferences": preference_catalog(),
        "preference_validation": preference_validation_report(),
        "demo": demo,
        "delivery_gate": delivery_gate(demo["draft"]),
        "calendar_policy": communication_calendar_policy(),
    }


def notification_center_demo(root: str = ".", db_path: str = "data/notification-center.db") -> dict:
    inbox = PortalInbox(db_path)
    demo = render_demo_notification()
    stored = inbox.store_draft(demo["draft"], "cust_demo")
    drafts = inbox.list_drafts("cust_demo")
    thread = thread_from_drafts("cust_demo", "Welcome and onboarding", [item["payload"] for item in drafts])
    export_path = write_notification_export(root)
    report_path = write_notification_report(root)
    audit = NotificationAuditLog(db_path).record("system", "notification.draft_created", demo["draft"]["id"], {"export_path": export_path})
    return {
        "draft": demo["draft"],
        "stored": stored,
        "drafts": drafts,
        "thread": thread.to_dict(),
        "delivery": delivery_gate(demo["draft"]),
        "schedule": schedule_notification_plan(demo["draft"]),
        "digest": digest_plan([demo["draft"]], "daily"),
        "export_path": export_path,
        "report_path": report_path,
        "export_bundle": notification_export_bundle(),
        "audit": audit.to_dict(),
    }
