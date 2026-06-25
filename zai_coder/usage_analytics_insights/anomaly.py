"""Simple deterministic anomaly detection."""

from __future__ import annotations


def detect_usage_anomalies(metrics: dict) -> dict:
    anomalies = []
    if metrics.get("total_events", 0) == 0:
        anomalies.append({"severity": "medium", "kind": "no_usage", "message": "No usage events recorded."})
    if metrics.get("active_customers", 0) == 0:
        anomalies.append({"severity": "medium", "kind": "no_active_customers", "message": "No active customers detected."})
    support_events = metrics.get("event_type_counts", {}).get("support.ticket", 0)
    feature_events = metrics.get("event_type_counts", {}).get("feature.use", 0)
    if support_events > feature_events and support_events >= 3:
        anomalies.append({"severity": "high", "kind": "support_spike", "message": "Support events exceed feature usage."})
    return {"ok": not anomalies, "anomalies": anomalies}


def anomaly_policy() -> dict:
    return {
        "deterministic": True,
        "no_external_ml_call": True,
        "support_spike_threshold": "support.ticket > feature.use and support.ticket >= 3",
        "human_review_required": True,
    }
