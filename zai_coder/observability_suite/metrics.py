"""Metrics registry and Prometheus-style renderer."""

from __future__ import annotations

from collections import OrderedDict

from .models import MetricSample


class MetricsRegistry:
    def __init__(self):
        self._samples: OrderedDict[str, MetricSample] = OrderedDict()

    def record(self, sample: MetricSample) -> MetricSample:
        issues = sample.validate()
        if issues:
            raise ValueError("; ".join(issues))
        key = self._key(sample.name, sample.labels)
        self._samples[key] = sample
        return sample

    def increment(self, name: str, amount: float = 1.0, labels: dict[str, str] | None = None) -> MetricSample:
        labels = labels or {}
        key = self._key(name, labels)
        current = self._samples.get(key)
        value = amount if current is None else current.value + amount
        return self.record(MetricSample(name=name, value=value, kind="counter", labels=labels))

    def gauge(self, name: str, value: float, labels: dict[str, str] | None = None) -> MetricSample:
        return self.record(MetricSample(name=name, value=value, kind="gauge", labels=labels or {}))

    def samples(self) -> list[MetricSample]:
        return list(self._samples.values())

    @staticmethod
    def _key(name: str, labels: dict[str, str]) -> str:
        label_part = ",".join(f"{k}={v}" for k, v in sorted(labels.items()))
        return f"{name}|{label_part}"


def render_prometheus_metrics(samples: list[MetricSample]) -> str:
    lines: list[str] = []
    seen_help: set[str] = set()
    for sample in samples:
        if sample.name not in seen_help:
            lines.append(f"# TYPE {sample.name} {sample.kind}")
            seen_help.add(sample.name)
        if sample.labels:
            labels = ",".join(f'{k}="{v}"' for k, v in sorted(sample.labels.items()))
            lines.append(f"{sample.name}{{{labels}}} {sample.value}")
        else:
            lines.append(f"{sample.name} {sample.value}")
    return "\n".join(lines) + ("\n" if lines else "")


def default_metrics_registry() -> MetricsRegistry:
    registry = MetricsRegistry()
    registry.gauge("zai_health_ok", 1, {"service": "control-plane"})
    registry.gauge("zai_queue_depth", 0, {"queue": "execution"})
    registry.increment("zai_build_info", 1, {"version": "v19"})
    return registry
