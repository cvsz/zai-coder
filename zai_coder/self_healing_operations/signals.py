"""Health signal evaluation."""

from __future__ import annotations

import uuid

from .models import HealthSignal


DEFAULT_THRESHOLDS = {
    "error_rate": {"warning": 0.02, "critical": 0.05},
    "latency_ms": {"warning": 750, "critical": 1500},
    "disk_usage_ratio": {"warning": 0.80, "critical": 0.92},
    "queue_depth": {"warning": 100, "critical": 500},
    "heartbeat_age_seconds": {"warning": 300, "critical": 900},
}


def classify_signal(metric: str, value: float) -> str:
    thresholds = DEFAULT_THRESHOLDS.get(metric)
    if not thresholds:
        return "unknown"
    if value >= thresholds["critical"]:
        return "critical"
    if value >= thresholds["warning"]:
        return "warning"
    return "ok"


def create_signal(source: str, metric: str, value: float, service: str = "core") -> HealthSignal:
    signal = HealthSignal(
        id=f"sig_{uuid.uuid4().hex[:12]}",
        source=source,
        metric=metric,
        value=value,
        status=classify_signal(metric, value),
        service=service,
    )
    issues = signal.validate()
    if issues:
        raise ValueError("; ".join(issues))
    return signal


def signal_summary(signals: list[HealthSignal]) -> dict:
    counts = {"ok": 0, "warning": 0, "critical": 0, "unknown": 0}
    for signal in signals:
        counts[signal.status] = counts.get(signal.status, 0) + 1
    worst = "critical" if counts["critical"] else "warning" if counts["warning"] else "unknown" if counts["unknown"] else "ok"
    return {"worst": worst, "counts": counts, "signals": [signal.to_dict() for signal in signals]}
