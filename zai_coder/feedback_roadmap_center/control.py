"""Feedback and Roadmap Center control helpers."""

from __future__ import annotations

from .feedback import FeedbackInbox, seed_demo_feedback
from .roadmap import roadmap_registry, roadmap_validation_report, roadmap_by_visibility
from .prioritization import prioritization_matrix
from .linker import link_feedback_to_roadmap, release_link_plan, release_link_gate
from .changelog_loop import changelog_feedback_prompt, changelog_feedback_summary
from .reporting import write_roadmap_report, roadmap_report_payload
from .exporter import write_roadmap_export, roadmap_export_bundle
from .audit import RoadmapAuditLog


def feedback_roadmap_status() -> dict:
    return {
        "ok": True,
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


def feedback_roadmap_overview() -> dict:
    feedback = seed_demo_feedback("data/feedback-roadmap-overview.db")
    roadmap = roadmap_registry()
    return {
        "status": feedback_roadmap_status(),
        "feedback_count": len(feedback),
        "roadmap": roadmap,
        "roadmap_validation": roadmap_validation_report(),
        "prioritization": prioritization_matrix(roadmap),
        "links": link_feedback_to_roadmap(feedback, roadmap),
        "customer_view": roadmap_by_visibility("customer"),
        "changelog_loop": changelog_feedback_summary(feedback),
    }


def feedback_roadmap_demo(db_path: str = "data/feedback-roadmap.db", root: str = ".") -> dict:
    feedback = seed_demo_feedback(db_path)
    roadmap = roadmap_registry()
    report = write_roadmap_report(feedback, root)
    export_path = write_roadmap_export(root, "customer")
    release = release_link_plan(roadmap[0]["id"], "v36.1.0")
    gate = release_link_gate(release.to_dict())
    audit = RoadmapAuditLog(db_path).record("system", "roadmap.report_generated", "feedback-roadmap", {"export_path": export_path})
    return {
        "feedback": feedback,
        "roadmap": roadmap,
        "report": report,
        "export_path": export_path,
        "export_bundle": roadmap_export_bundle("customer"),
        "release_link": release.to_dict(),
        "release_gate": gate,
        "audit": audit.to_dict(),
    }
