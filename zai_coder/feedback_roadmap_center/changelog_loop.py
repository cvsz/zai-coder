"""Changelog feedback loop."""

from __future__ import annotations


def changelog_feedback_prompt(release_version: str = "v36.0.0") -> dict:
    return {
        "dry_run": True,
        "release_version": release_version,
        "questions": [
            "Which shipped item delivered the most customer value?",
            "Which roadmap item remains unclear?",
            "Which onboarding step still creates friction?",
            "Which integration should be prioritized next?",
        ],
        "send": False,
    }


def changelog_feedback_summary(feedback_items: list[dict]) -> dict:
    categories = {}
    sentiment = {"positive": 0, "neutral": 0, "negative": 0}
    for item in feedback_items:
        categories[item["category"]] = categories.get(item["category"], 0) + 1
        sentiment[item["sentiment"]] = sentiment.get(item["sentiment"], 0) + 1
    return {
        "feedback_count": len(feedback_items),
        "categories": categories,
        "sentiment": sentiment,
        "roadmap_recommendation": "Prioritize high-frequency categories with negative or high-priority signals.",
    }
