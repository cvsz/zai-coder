"""Alert rules and evaluator."""

from __future__ import annotations

from .models import AlertRule, MetricSample


DEFAULT_ALERT_RULES = [
    AlertRule("execution_queue_depth_high", "zai_queue_depth", ">", 100, "warning", 300),
    AlertRule("health_down", "zai_health_ok", "<", 1, "critical", 60),
    AlertRule("provider_failures_high", "zai_provider_failures_total", ">", 5, "warning", 600),
]


def evaluate_alerts(samples: list[MetricSample], rules: list[AlertRule] | None = None) -> list[dict]:
    rules = rules or DEFAULT_ALERT_RULES
    by_metric = {sample.name: sample for sample in samples}
    triggered: list[dict] = []
    for rule in rules:
        sample = by_metric.get(rule.metric)
        if sample and rule.evaluate(sample.value):
            triggered.append({"rule": rule.to_dict(), "sample": sample.to_dict(), "triggered": True})
    return triggered


def alert_rules_manifest() -> list[dict]:
    return [rule.to_dict() for rule in DEFAULT_ALERT_RULES]
