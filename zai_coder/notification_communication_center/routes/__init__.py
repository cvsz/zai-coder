"""Notification and Communication Center route registry."""

from __future__ import annotations

from zai_coder.notification_communication_center.control import notification_center_status, notification_center_overview, notification_center_demo
from zai_coder.notification_communication_center.channels import channel_catalog, channel_policy, channel_validation_report
from zai_coder.notification_communication_center.templates import notification_template_registry, notification_template_validation_report, templates_by_channel
from zai_coder.notification_communication_center.preferences import preference_catalog, preference_validation_report, preference_decision
from zai_coder.notification_communication_center.render import render_demo_notification
from zai_coder.notification_communication_center.delivery import delivery_gate, digest_plan
from zai_coder.notification_communication_center.scheduler import schedule_notification_plan, communication_calendar_policy
from zai_coder.notification_communication_center.exporter import notification_export_bundle, write_notification_export, write_notification_report
from zai_coder.notification_communication_center.audit import NotificationAuditLog
from zai_coder.notification_communication_center.ui.pages import render_notifications_overview_page, render_channels_page, render_templates_page, render_preferences_page, render_drafts_page


def route_notification_center_status() -> dict:
    return {
        "ok": True,
        "service": "zai-notification-and-communication-center",
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


def route_notification_center_overview() -> dict:
    return notification_center_overview()


def route_notification_channels() -> dict:
    return {"channels": channel_catalog(), "validation": channel_validation_report(), "email_policy": channel_policy("email")}


def route_notification_templates() -> dict:
    return {"templates": notification_template_registry(), "portal": templates_by_channel("portal"), "validation": notification_template_validation_report()}


def route_notification_preferences() -> dict:
    return {"preferences": preference_catalog(), "validation": preference_validation_report(), "decision": preference_decision("cust_demo", "portal", "product")}


def route_notification_render_demo() -> dict:
    return render_demo_notification()


def route_notification_delivery() -> dict:
    draft = render_demo_notification()["draft"]
    return {"gate": delivery_gate(draft), "schedule": schedule_notification_plan(draft), "digest": digest_plan([draft])}


def route_notification_export() -> dict:
    return {"bundle": notification_export_bundle(), "export_path": write_notification_export("."), "report_path": write_notification_report(".")}


def route_notification_demo() -> dict:
    return notification_center_demo(".", "data/notification-center-demo.db")


def route_notification_audit() -> dict:
    return {"events": NotificationAuditLog().list_events()}


def route_notifications_page() -> dict:
    return {"content_type": "text/html", "html": render_notifications_overview_page()}


def route_notifications_channels_page() -> dict:
    return {"content_type": "text/html", "html": render_channels_page()}


def route_notifications_templates_page() -> dict:
    return {"content_type": "text/html", "html": render_templates_page()}


def route_notifications_preferences_page() -> dict:
    return {"content_type": "text/html", "html": render_preferences_page()}


def route_notifications_drafts_page() -> dict:
    return {"content_type": "text/html", "html": render_drafts_page()}
