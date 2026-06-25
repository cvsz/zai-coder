"""Adoption funnel and activation analytics."""

from __future__ import annotations


DEFAULT_FUNNEL_STEPS = ["portal.view", "onboarding.step", "feature.use", "support.ticket"]


def adoption_funnel(events: list[dict], steps: list[str] | None = None) -> dict:
    steps = steps or DEFAULT_FUNNEL_STEPS
    customers_by_step = {}
    for step in steps:
        customers_by_step[step] = {event["customer_id"] for event in events if event["event_type"] == step}
    counts = {step: len(customers) for step, customers in customers_by_step.items()}
    conversions = {}
    for idx, step in enumerate(steps):
        if idx == 0:
            conversions[step] = 1.0 if counts[step] else 0.0
        else:
            prev = counts[steps[idx - 1]]
            conversions[step] = 0.0 if prev == 0 else round(counts[step] / prev, 4)
    return {"steps": steps, "counts": counts, "conversions": conversions}


def activation_score(events: list[dict], customer_id: str) -> dict:
    customer_events = [event for event in events if event["customer_id"] == customer_id]
    feature_count = len({event["feature_id"] for event in customer_events})
    event_count = len(customer_events)
    support_count = sum(1 for event in customer_events if event["event_type"] == "support.ticket")
    score = min(100, event_count * 10 + feature_count * 15 - support_count * 5)
    status = "activated" if score >= 50 else "warming" if score >= 25 else "needs_attention"
    return {"customer_id": customer_id, "score": score, "status": status, "event_count": event_count, "feature_count": feature_count}
