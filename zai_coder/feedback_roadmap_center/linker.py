"""Feedback-to-roadmap and roadmap-to-release linkage."""

from __future__ import annotations

import uuid

from .models import ReleaseLink


def link_feedback_to_roadmap(feedback_items: list[dict], roadmap_items: list[dict]) -> dict:
    links = []
    for feedback in feedback_items:
        matched = None
        for roadmap in roadmap_items:
            text = (feedback["title"] + " " + feedback["body"]).lower()
            if roadmap["theme"] in text or any(word in text for word in roadmap["title"].lower().split()[:2]):
                matched = roadmap["id"]
                break
        if matched:
            links.append({"feedback_id": feedback["id"], "roadmap_id": matched, "confidence": "medium"})
    return {"links": links, "unlinked": [item["id"] for item in feedback_items if item["id"] not in {link["feedback_id"] for link in links}]}


def release_link_plan(roadmap_id: str, target_version: str = "v36.1.0", release_channel: str = "stable") -> ReleaseLink:
    link = ReleaseLink(f"rl_{uuid.uuid4().hex[:12]}", roadmap_id, target_version, release_channel, "draft")
    issues = link.validate()
    if issues:
        raise ValueError("; ".join(issues))
    return link


def release_link_gate(link_payload: dict, approval_id: str = "", apply_requested: bool = False) -> dict:
    blocked = []
    if apply_requested:
        blocked.append("release links cannot be applied by roadmap center")
    if not approval_id.startswith("approved_") and link_payload.get("status") != "draft":
        blocked.append("non-draft release link requires approval")
    return {"allowed": not blocked, "blocked": blocked, "link": link_payload}
