from pathlib import Path

from zai_coder.notification_communication_center.models import NotificationTemplate, NotificationPreference, NotificationDraft, CommunicationThread
from zai_coder.notification_communication_center.channels import channel_catalog, channel_policy, channel_validation_report
from zai_coder.notification_communication_center.templates import notification_template_registry, notification_template_validation_report, notification_template_by_id, templates_by_channel
from zai_coder.notification_communication_center.preferences import preference_catalog, preference_validation_report, preference_decision
from zai_coder.notification_communication_center.render import extract_notification_variables, validate_notification_variables, render_text, render_notification_draft, render_demo_notification
from zai_coder.notification_communication_center.delivery import delivery_gate, digest_plan
from zai_coder.notification_communication_center.inbox import PortalInbox, thread_from_drafts
from zai_coder.notification_communication_center.scheduler import schedule_notification_plan, communication_calendar_policy
from zai_coder.notification_communication_center.exporter import notification_export_bundle, write_notification_export, write_notification_report
from zai_coder.notification_communication_center.audit import NotificationAuditLog
from zai_coder.notification_communication_center.control import notification_center_status, notification_center_overview, notification_center_demo
from zai_coder.notification_communication_center.ui.pages import render_notifications_overview_page, render_channels_page, render_templates_page, render_preferences_page, render_drafts_page
from zai_coder.notification_communication_center.routes import (
    route_notification_center_status,
    route_notification_center_overview,
    route_notification_channels,
    route_notification_templates,
    route_notification_preferences,
    route_notification_render_demo,
    route_notification_delivery,
    route_notification_export,
    route_notification_demo,
    route_notification_audit,
    route_notifications_page,
    route_notifications_channels_page,
    route_notifications_templates_page,
    route_notifications_preferences_page,
    route_notifications_drafts_page,
)


def test_models_validation():
    assert NotificationTemplate("t", "Title", "portal", "Subject", "Body").validate() == []
    assert NotificationTemplate("", "", "bad", "token", "secret", audience="bad", status="bad", visibility="bad").validate()
    assert NotificationPreference("p", "cust", "portal").validate() == []
    assert NotificationPreference("", "", "bad", topic="bad", frequency="bad").validate()
    assert NotificationDraft("d", "t", "portal", "Subject", "Body", "cust").validate() == []
    assert NotificationDraft("", "", "bad", "token", "secret", "", status="bad", dry_run=False).validate()
    assert CommunicationThread("th", "cust", "Subject").validate() == []


def test_channels_templates_preferences_rendering():
    assert channel_catalog()
    assert channel_validation_report()["ok"] is True
    assert channel_policy("portal")["send_enabled"] is True
    assert channel_policy("email")["external_delivery_disabled"] is True
    assert notification_template_registry()
    assert notification_template_validation_report()["ok"] is True
    assert notification_template_by_id("ntpl-welcome").id == "ntpl-welcome"
    assert templates_by_channel("portal")
    assert preference_catalog()
    assert preference_validation_report()["ok"] is True
    assert preference_decision("cust_demo", "portal", "product")["allowed"] is True
    assert preference_decision("cust_demo", "email", "product")["allowed"] is False
    assert "customer_name" in extract_notification_variables("Hi {{customer_name}}")
    tpl = notification_template_by_id("ntpl-welcome").to_dict()
    good_vars = {"customer_name": "Demo", "product_name": "ZAI Coder Control Plane", "next_step": "review local-first checklist"}
    assert validate_notification_variables(tpl, good_vars)["ok"] is True
    assert validate_notification_variables(tpl, {"customer_name": "Demo"})["ok"] is False
    assert render_text("Hi {{name}}", {"name": "Demo"}) == "Hi Demo"
    draft = render_notification_draft("ntpl-welcome", "cust_demo", "cust_demo", "product", good_vars)
    assert draft.dry_run is True
    assert route_notification_render_demo()["draft"]["dry_run"] is True


def test_delivery_inbox_scheduler_export_audit(tmp_path):
    draft = render_demo_notification()["draft"]
    assert delivery_gate(draft)["allowed"] is True
    email_draft = {**draft, "channel": "email"}
    assert delivery_gate(email_draft)["allowed"] is False
    assert delivery_gate(draft, send_requested=True)["allowed"] is False
    assert digest_plan([draft], "daily")["send"] is False
    assert schedule_notification_plan(draft)["scheduled"] is False
    assert communication_calendar_policy()["no_external_calendar_write"] is True
    inbox = PortalInbox(tmp_path / "notifications.db")
    stored = inbox.store_draft(draft, "cust_demo")
    assert stored["stored"] is True
    drafts = inbox.list_drafts("cust_demo")
    assert drafts
    thread = thread_from_drafts("cust_demo", "Welcome", [row["payload"] for row in drafts])
    assert thread.customer_id == "cust_demo"
    bundle = notification_export_bundle()
    assert bundle["external_send"] is False
    export_path = write_notification_export(tmp_path)
    report_path = write_notification_report(tmp_path)
    assert Path(export_path).exists()
    assert Path(report_path).exists()
    audit = NotificationAuditLog(tmp_path / "notifications.db")
    event = audit.record("tester", "notification.test", draft["id"])
    assert audit.list_events()[0]["id"] == event.id


def test_control_ui_routes(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    assert notification_center_status()["ok"] is True
    overview = notification_center_overview()
    assert overview["status"]["ok"] is True
    demo = notification_center_demo(str(tmp_path), str(tmp_path / "notification.db"))
    assert Path(demo["export_path"]).exists()
    assert Path(demo["report_path"]).exists()
    assert "Notification and Communication Center" in render_notifications_overview_page()
    assert "Channels" in render_channels_page()
    assert "Templates" in render_templates_page()
    assert "Preferences" in render_preferences_page()
    assert "Drafts" in render_drafts_page()
    assert route_notification_center_status()["ok"] is True
    assert route_notification_center_overview()["status"]["ok"] is True
    assert route_notification_channels()["validation"]["ok"] is True
    assert route_notification_templates()["validation"]["ok"] is True
    assert route_notification_preferences()["decision"]["allowed"] is True
    assert route_notification_delivery()["gate"]["allowed"] is True
    assert Path(route_notification_export()["export_path"]).exists()
    assert Path(route_notification_demo()["export_path"]).exists()
    assert "events" in route_notification_audit()
    assert route_notifications_page()["content_type"] == "text/html"
    assert route_notifications_channels_page()["content_type"] == "text/html"
    assert route_notifications_templates_page()["content_type"] == "text/html"
    assert route_notifications_preferences_page()["content_type"] == "text/html"
    assert route_notifications_drafts_page()["content_type"] == "text/html"


def test_docs_scripts_assets_exist():
    root = Path(__file__).resolve().parents[1]
    for rel in [
        "scripts/notification-center/notification-status.sh",
        "scripts/notification-center/notification-channels.sh",
        "scripts/notification-center/notification-templates.sh",
        "scripts/notification-center/notification-preferences.sh",
        "scripts/notification-center/notification-render-demo.sh",
        "scripts/notification-center/notification-delivery.sh",
        "scripts/notification-center/notification-demo.sh",
        "scripts/notification-center/notification-export.sh",
        "scripts/notification-center/notification-audit.sh",
        "scripts/notification-center/notification-dashboard-export.sh",
        "docs/notification-center/NOTIFICATION_COMMUNICATION_CENTER_GUIDE.md",
        "docs/notification-center/CHANNEL_POLICY.md",
        "docs/notification-center/PREFERENCE_CENTER.md",
        "docs/notification-center/DRAFT_DELIVERY_GATE.md",
        "docs/notification-center/PORTAL_INBOX.md",
        "docs/notification-center/COMMUNICATION_EXPORT_POLICY.md",
        "docs/requirements/NEXT_V39_NOTIFICATION_COMMUNICATION_CENTER_REQUIREMENTS.md",
        "assets/notification-center/notification_communication_center_features.json",
    ]:
        assert (root / rel).exists(), rel
