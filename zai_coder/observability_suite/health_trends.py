"""Health trend snapshots."""

from __future__ import annotations

from dataclasses import dataclass, field

from .models import now_iso


@dataclass(frozen=True)
class HealthSnapshot:
    status: str
    checks_total: int
    checks_ok: int
    latency_ms: float = 0
    ts: str = field(default_factory=now_iso)

    @property
    def ok_ratio(self) -> float:
        if self.checks_total <= 0:
            return 0.0
        return self.checks_ok / self.checks_total

    def to_dict(self) -> dict:
        return {"status": self.status, "checks_total": self.checks_total, "checks_ok": self.checks_ok, "ok_ratio": self.ok_ratio, "latency_ms": self.latency_ms, "ts": self.ts}


class HealthTrendStore:
    def __init__(self):
        self._snapshots: list[HealthSnapshot] = []

    def add(self, snapshot: HealthSnapshot) -> HealthSnapshot:
        self._snapshots.append(snapshot)
        return snapshot

    def list_snapshots(self, limit: int = 50) -> list[dict]:
        return [snapshot.to_dict() for snapshot in self._snapshots[-limit:]]

    def summary(self) -> dict:
        if not self._snapshots:
            return {"ok": True, "snapshots": 0, "latest": None}
        latest = self._snapshots[-1]
        return {"ok": latest.status == "ok", "snapshots": len(self._snapshots), "latest": latest.to_dict()}


def default_health_trend_store() -> HealthTrendStore:
    store = HealthTrendStore()
    store.add(HealthSnapshot("ok", 5, 5, 12.5))
    store.add(HealthSnapshot("ok", 5, 5, 13.2))
    return store
