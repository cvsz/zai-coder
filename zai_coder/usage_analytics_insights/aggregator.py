"""Metric aggregation for usage analytics."""

from __future__ import annotations

import uuid
from collections import Counter, defaultdict

from .models import MetricSnapshot


def aggregate_usage(events: list[dict], period: str = "current") -> dict:
    total_events = len(events)
    total_quantity = sum(float(event.get("quantity", 0)) for event in events)
    active_customers = len({event["customer_id"] for event in events})
    active_workspaces = len({event["workspace_id"] for event in events})
    feature_counts = Counter(event["feature_id"] for event in events)
    event_type_counts = Counter(event["event_type"] for event in events)
    return {
        "period": period,
        "total_events": total_events,
        "total_quantity": total_quantity,
        "active_customers": active_customers,
        "active_workspaces": active_workspaces,
        "feature_counts": dict(feature_counts),
        "event_type_counts": dict(event_type_counts),
    }


def metric_snapshots(events: list[dict], period: str = "current") -> list[dict]:
    agg = aggregate_usage(events, period)
    rows = [
        MetricSnapshot(f"met_{uuid.uuid4().hex[:12]}", "total_events", agg["total_events"], period, unit="events"),
        MetricSnapshot(f"met_{uuid.uuid4().hex[:12]}", "total_quantity", agg["total_quantity"], period, unit="units"),
        MetricSnapshot(f"met_{uuid.uuid4().hex[:12]}", "active_customers", agg["active_customers"], period, unit="customers"),
        MetricSnapshot(f"met_{uuid.uuid4().hex[:12]}", "active_workspaces", agg["active_workspaces"], period, unit="workspaces"),
    ]
    for feature, count in agg["feature_counts"].items():
        rows.append(MetricSnapshot(f"met_{uuid.uuid4().hex[:12]}", f"feature.{feature}", count, period, unit="events"))
    reports = [{"id": row.id, "issues": row.validate()} for row in rows]
    if any(item["issues"] for item in reports):
        raise ValueError(str(reports))
    return [row.to_dict() for row in rows]


def customer_breakdown(events: list[dict]) -> dict:
    grouped = defaultdict(list)
    for event in events:
        grouped[event["customer_id"]].append(event)
    return {customer_id: aggregate_usage(rows, "customer") for customer_id, rows in grouped.items()}
