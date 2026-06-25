"""Usage insights generator."""

from __future__ import annotations

import uuid

from .models import Insight
from .aggregator import aggregate_usage, customer_breakdown
from .funnels import adoption_funnel, activation_score
from .anomaly import detect_usage_anomalies


def generate_insights(events: list[dict]) -> list[dict]:
    metrics = aggregate_usage(events)
    funnel = adoption_funnel(events)
    anomalies = detect_usage_anomalies(metrics)
    insights: list[Insight] = []

    if metrics["active_customers"] > 0:
        insights.append(Insight(
            f"ins_{uuid.uuid4().hex[:12]}",
            "Active customer usage detected",
            "info",
            "usage",
            f"{metrics['active_customers']} active customers generated {metrics['total_events']} events.",
            "Review customer-level activation to identify expansion opportunities.",
        ))

    if funnel["conversions"].get("feature.use", 0) < 1.0:
        insights.append(Insight(
            f"ins_{uuid.uuid4().hex[:12]}",
            "Feature adoption funnel has drop-off",
            "medium",
            "adoption",
            "Not every onboarding customer reached feature usage.",
            "Improve onboarding checklist and connector setup guidance.",
        ))

    for anomaly in anomalies["anomalies"]:
        insights.append(Insight(
            f"ins_{uuid.uuid4().hex[:12]}",
            anomaly["kind"].replace("_", " ").title(),
            anomaly["severity"],
            "risk",
            anomaly["message"],
            "Review the anomaly before taking action.",
        ))

    for customer_id in customer_breakdown(events):
        activation = activation_score(events, customer_id)
        if activation["status"] == "needs_attention":
            insights.append(Insight(
                f"ins_{uuid.uuid4().hex[:12]}",
                f"Customer {customer_id} needs activation attention",
                "medium",
                "growth",
                f"Activation score is {activation['score']}.",
                "Trigger onboarding follow-up plan; do not send external messages automatically.",
            ))

    reports = [{"id": item.id, "issues": item.validate()} for item in insights]
    if any(item["issues"] for item in reports):
        raise ValueError(str(reports))
    return [item.to_dict() for item in insights]
