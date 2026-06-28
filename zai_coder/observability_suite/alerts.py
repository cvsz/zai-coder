"""Alert rules and evaluator."""

from __future__ import annotations

from .models import AlertRule, MetricSample


DEFAULT_ALERT_RULES = [
    AlertRule("execution_queue_depth_high", "zai_queue_depth", ">", 100, "warning", 300),
    AlertRule("health_down", "zai_health_ok", "<", 1, "critical", 60),
    AlertRule("provider_failures_high", "zai_provider_failures_total", ">", 5, "warning", 600),
]


import time

class AlertManager:
    def __init__(self):
        self._active_alerts = {}
        self._incident_queue = []
        self._rate_limits = {}  # rule_name -> last trigger timestamp
        self.rate_limit_seconds = 60

    def evaluate_alerts(self, samples: list[MetricSample], rules: list[AlertRule] | None = None) -> list[dict]:
        rules = rules or DEFAULT_ALERT_RULES
        by_metric = {sample.name: sample for sample in samples}
        triggered: list[dict] = []
        now = time.time()
        
        for rule in rules:
            sample = by_metric.get(rule.metric)
            if sample and rule.evaluate(sample.value):
                # Deduplication and rate limiting
                last_triggered = self._rate_limits.get(rule.name, 0)
                if now - last_triggered > self.rate_limit_seconds:
                    self._rate_limits[rule.name] = now
                    incident = {"rule": rule.to_dict(), "sample": sample.to_dict(), "triggered": True, "ts": now}
                    triggered.append(incident)
                    self._incident_queue.append(incident)
        return triggered

    def get_incident_queue(self) -> list[dict]:
        return self._incident_queue

    def clear_incident_queue(self):
        self._incident_queue = []

_default_manager = AlertManager()

def evaluate_alerts(samples: list[MetricSample], rules: list[AlertRule] | None = None) -> list[dict]:
    return _default_manager.evaluate_alerts(samples, rules)

def alert_rules_manifest() -> list[dict]:
    return [rule.to_dict() for rule in DEFAULT_ALERT_RULES]
