from pathlib import Path

from zai_coder.feedback_roadmap_center.models import FeedbackItem, RoadmapItem, PriorityScore, ReleaseLink
from zai_coder.feedback_roadmap_center.feedback import FeedbackInbox, seed_demo_feedback, feedback_triage
from zai_coder.feedback_roadmap_center.roadmap import roadmap_registry, roadmap_validation_report, roadmap_by_visibility, roadmap_by_horizon
from zai_coder.feedback_roadmap_center.prioritization import rice_score, score_roadmap_item, prioritization_matrix
from zai_coder.feedback_roadmap_center.linker import link_feedback_to_roadmap, release_link_plan, release_link_gate
from zai_coder.feedback_roadmap_center.changelog_loop import changelog_feedback_prompt, changelog_feedback_summary
from zai_coder.feedback_roadmap_center.reporting import roadmap_report_payload, roadmap_report_markdown, write_roadmap_report
from zai_coder.feedback_roadmap_center.exporter import roadmap_export_bundle, write_roadmap_export
from zai_coder.feedback_roadmap_center.audit import RoadmapAuditLog
from zai_coder.feedback_roadmap_center.control import feedback_roadmap_status, feedback_roadmap_overview, feedback_roadmap_demo
from zai_coder.feedback_roadmap_center.ui.pages import render_roadmap_overview_page, render_feedback_page, render_roadmap_items_page, render_customer_view_page, render_prioritization_page
from zai_coder.feedback_roadmap_center.routes import (
    route_feedback_roadmap_status,
    route_feedback_roadmap_overview,
    route_feedback_seed_demo,
    route_feedback_triage,
    route_roadmap_items,
    route_roadmap_customer_view,
    route_roadmap_prioritization,
    route_feedback_links,
    route_release_link_plan,
    route_changelog_feedback_loop,
    route_roadmap_report_demo,
    route_roadmap_report_markdown,
    route_roadmap_export,
    route_roadmap_audit,
    route_roadmap_page,
    route_roadmap_feedback_page,
    route_roadmap_items_page,
    route_roadmap_customer_view_page,
    route_roadmap_prioritization_page,
)


def test_models_validation():
    assert FeedbackItem("f", "c", "Title", "Body").validate() == []
    assert FeedbackItem("", "", "", "token here", category="bad", sentiment="bad", priority_hint="bad", status="bad").validate()
    assert RoadmapItem("r", "Title", "Description").validate() == []
    assert RoadmapItem("", "", "", status="bad", horizon="bad", visibility="bad").validate()
    assert PriorityScore("p", "r", 1, 1, 1, 1, 1).validate() == []
    assert PriorityScore("", "", 0, 0, 0, 0, -1, method="bad").validate()
    assert ReleaseLink("l", "r", "v1.0.0").validate() == []
    assert ReleaseLink("", "", "1.0.0", "bad", "bad").validate()


def test_feedback_inbox_roadmap_prioritization(tmp_path):
    inbox = FeedbackInbox(tmp_path / "roadmap.db")
    item = inbox.submit_feedback("cust", "Need feature", "Please add roadmap export.", "feature", "neutral", "high")
    assert item.id.startswith("fb_")
    assert inbox.list_feedback("cust")[0]["id"] == item.id
    try:
        inbox.submit_feedback("cust", "Contains token", "token abc")
        assert False
    except ValueError:
        assert True
    feedback = seed_demo_feedback(tmp_path / "roadmap2.db")
    triage = feedback_triage(feedback[0])
    assert triage["queue"] in {"critical_review", "product_review", "backlog"}
    roadmap = roadmap_registry()
    assert roadmap
    assert roadmap_validation_report()["ok"] is True
    assert all(item["visibility"] != "private" for item in roadmap_by_visibility("customer"))
    assert roadmap_by_horizon("next")
    assert rice_score(10, 3, 8, 5) == 48
    score = score_roadmap_item("rm", 10, 3, 8, 5)
    assert score.score == 48
    assert prioritization_matrix(roadmap)["scores"]


def test_linking_changelog_reporting_export_audit(tmp_path):
    feedback = seed_demo_feedback(tmp_path / "roadmap.db")
    roadmap = roadmap_registry()
    links = link_feedback_to_roadmap(feedback, roadmap)
    assert "links" in links
    release = release_link_plan(roadmap[0]["id"], "v36.1.0")
    assert release.target_version == "v36.1.0"
    assert release_link_gate(release.to_dict())["allowed"] is True
    assert release_link_gate({**release.to_dict(), "status": "approved"})["allowed"] is False
    prompt = changelog_feedback_prompt("v36.0.0")
    assert prompt["send"] is False
    summary = changelog_feedback_summary(feedback)
    assert summary["feedback_count"] == len(feedback)
    payload = roadmap_report_payload(feedback)
    assert payload["external_publish"] is False
    assert "Feedback and Roadmap" in roadmap_report_markdown(feedback)
    report_paths = write_roadmap_report(feedback, tmp_path)
    assert Path(report_paths["json"]).exists()
    assert Path(report_paths["markdown"]).exists()
    bundle = roadmap_export_bundle("customer")
    assert bundle["external_publish"] is False
    export_path = write_roadmap_export(tmp_path, "customer")
    assert Path(export_path).exists()
    audit = RoadmapAuditLog(tmp_path / "roadmap-audit.db")
    event = audit.record("tester", "roadmap.test", "target")
    assert audit.list_events()[0]["id"] == event.id


def test_control_ui_routes(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    assert feedback_roadmap_status()["ok"] is True
    overview = feedback_roadmap_overview()
    assert overview["status"]["ok"] is True
    demo = feedback_roadmap_demo(str(tmp_path / "demo.db"), str(tmp_path))
    assert Path(demo["report"]["json"]).exists()
    assert Path(demo["export_path"]).exists()
    assert "Feedback and Roadmap Center" in render_roadmap_overview_page()
    assert "Feedback" in render_feedback_page()
    assert "Roadmap" in render_roadmap_items_page()
    assert "Customer View" in render_customer_view_page()
    assert "Prioritization" in render_prioritization_page()
    assert route_feedback_roadmap_status()["ok"] is True
    assert route_feedback_roadmap_overview()["status"]["ok"] is True
    assert route_feedback_seed_demo()["feedback"]
    assert route_feedback_triage()["triage"]
    assert route_roadmap_items()["validation"]["ok"] is True
    assert route_roadmap_customer_view()["customer"]
    assert route_roadmap_prioritization()["scores"]
    assert "links" in route_feedback_links()
    assert route_release_link_plan()["gate"]["allowed"] is True
    assert route_changelog_feedback_loop()["prompt"]["send"] is False
    assert Path(route_roadmap_report_demo()["report"]["json"]).exists()
    assert "markdown" in route_roadmap_report_markdown()
    assert Path(route_roadmap_export()["path"]).exists()
    assert "events" in route_roadmap_audit()
    assert route_roadmap_page()["content_type"] == "text/html"
    assert route_roadmap_feedback_page()["content_type"] == "text/html"
    assert route_roadmap_items_page()["content_type"] == "text/html"
    assert route_roadmap_customer_view_page()["content_type"] == "text/html"
    assert route_roadmap_prioritization_page()["content_type"] == "text/html"


def test_docs_scripts_assets_exist():
    root = Path(__file__).resolve().parents[1]
    for rel in [
        "scripts/feedback-roadmap/roadmap-status.sh",
        "scripts/feedback-roadmap/feedback-seed-demo.sh",
        "scripts/feedback-roadmap/feedback-triage.sh",
        "scripts/feedback-roadmap/roadmap-items.sh",
        "scripts/feedback-roadmap/roadmap-customer-view.sh",
        "scripts/feedback-roadmap/roadmap-prioritization.sh",
        "scripts/feedback-roadmap/feedback-links.sh",
        "scripts/feedback-roadmap/release-link-plan.sh",
        "scripts/feedback-roadmap/changelog-feedback-loop.sh",
        "scripts/feedback-roadmap/roadmap-report-demo.sh",
        "scripts/feedback-roadmap/roadmap-report-markdown.sh",
        "scripts/feedback-roadmap/roadmap-export.sh",
        "scripts/feedback-roadmap/roadmap-audit.sh",
        "scripts/feedback-roadmap/roadmap-dashboard-export.sh",
        "docs/feedback-roadmap/FEEDBACK_ROADMAP_CENTER_GUIDE.md",
        "docs/feedback-roadmap/FEEDBACK_INBOX.md",
        "docs/feedback-roadmap/ROADMAP_REGISTRY.md",
        "docs/feedback-roadmap/PRIORITIZATION.md",
        "docs/feedback-roadmap/CUSTOMER_ROADMAP_VIEW.md",
        "docs/feedback-roadmap/CHANGELOG_FEEDBACK_LOOP.md",
        "docs/requirements/NEXT_V36_FEEDBACK_ROADMAP_CENTER_REQUIREMENTS.md",
        "assets/feedback-roadmap/feedback_roadmap_center_features.json",
    ]:
        assert (root / rel).exists(), rel
