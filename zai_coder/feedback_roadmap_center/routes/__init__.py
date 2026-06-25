"""Feedback and Roadmap Center route registry."""

from __future__ import annotations

from zai_coder.feedback_roadmap_center.control import feedback_roadmap_status, feedback_roadmap_overview, feedback_roadmap_demo
from zai_coder.feedback_roadmap_center.feedback import FeedbackInbox, seed_demo_feedback, feedback_triage
from zai_coder.feedback_roadmap_center.roadmap import roadmap_registry, roadmap_validation_report, roadmap_by_visibility, roadmap_by_horizon
from zai_coder.feedback_roadmap_center.prioritization import prioritization_matrix
from zai_coder.feedback_roadmap_center.linker import link_feedback_to_roadmap, release_link_plan, release_link_gate
from zai_coder.feedback_roadmap_center.changelog_loop import changelog_feedback_prompt, changelog_feedback_summary
from zai_coder.feedback_roadmap_center.reporting import roadmap_report_payload, roadmap_report_markdown, write_roadmap_report
from zai_coder.feedback_roadmap_center.exporter import roadmap_export_bundle, write_roadmap_export
from zai_coder.feedback_roadmap_center.audit import RoadmapAuditLog
from zai_coder.feedback_roadmap_center.ui.pages import render_roadmap_overview_page, render_feedback_page, render_roadmap_items_page, render_customer_view_page, render_prioritization_page


def route_feedback_roadmap_status() -> dict:
    return {
        "ok": True,
        "service": "zai-feedback-and-roadmap-center",
        "systems": [
            "feedback_inbox",
            "customer_request_triage",
            "roadmap_registry",
            "prioritization_scoring",
            "feedback_roadmap_linker",
            "release_planning_linkage",
            "public_private_roadmap_views",
            "changelog_feedback_loop",
            "roadmap_exports",
            "roadmap_audit_log",
        ],
    }


def route_feedback_roadmap_overview() -> dict:
    return feedback_roadmap_overview()


def route_feedback_seed_demo() -> dict:
    return {"feedback": seed_demo_feedback()}


def route_feedback_triage() -> dict:
    feedback = seed_demo_feedback("data/feedback-roadmap-triage.db")
    return {"triage": [feedback_triage(item) for item in feedback]}


def route_roadmap_items() -> dict:
    return {"roadmap": roadmap_registry(), "validation": roadmap_validation_report(), "now": roadmap_by_horizon("now"), "next": roadmap_by_horizon("next")}


def route_roadmap_customer_view() -> dict:
    return {"customer": roadmap_by_visibility("customer"), "public": roadmap_by_visibility("public")}


def route_roadmap_prioritization() -> dict:
    return prioritization_matrix(roadmap_registry())


def route_feedback_links() -> dict:
    feedback = seed_demo_feedback("data/feedback-roadmap-links.db")
    return link_feedback_to_roadmap(feedback, roadmap_registry())


def route_release_link_plan() -> dict:
    link = release_link_plan("rm-roadmap-public", "v36.1.0")
    return {"link": link.to_dict(), "gate": release_link_gate(link.to_dict())}


def route_changelog_feedback_loop() -> dict:
    feedback = seed_demo_feedback("data/feedback-roadmap-changelog.db")
    return {"prompt": changelog_feedback_prompt("v36.0.0"), "summary": changelog_feedback_summary(feedback)}


def route_roadmap_report_demo() -> dict:
    return feedback_roadmap_demo("data/feedback-roadmap-report.db", ".")


def route_roadmap_report_markdown() -> dict:
    feedback = seed_demo_feedback("data/feedback-roadmap-md.db")
    return {"markdown": roadmap_report_markdown(feedback), "payload": roadmap_report_payload(feedback)}


def route_roadmap_export() -> dict:
    return {"bundle": roadmap_export_bundle("customer"), "path": write_roadmap_export(".", "customer")}


def route_roadmap_audit() -> dict:
    return {"events": RoadmapAuditLog().list_events()}


def route_roadmap_page() -> dict:
    return {"content_type": "text/html", "html": render_roadmap_overview_page()}


def route_roadmap_feedback_page() -> dict:
    return {"content_type": "text/html", "html": render_feedback_page()}


def route_roadmap_items_page() -> dict:
    return {"content_type": "text/html", "html": render_roadmap_items_page()}


def route_roadmap_customer_view_page() -> dict:
    return {"content_type": "text/html", "html": render_customer_view_page()}


def route_roadmap_prioritization_page() -> dict:
    return {"content_type": "text/html", "html": render_prioritization_page()}
