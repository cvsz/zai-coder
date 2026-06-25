"""Agent heartbeat and stale detection."""

from __future__ import annotations

from datetime import datetime, timezone


def parse_iso(ts: str) -> datetime:
    return datetime.fromisoformat(ts.replace("Z", "+00:00"))


def heartbeat_decision(heartbeat_at: str, stale_seconds: int = 300) -> dict:
    now = datetime.now(timezone.utc)
    last = parse_iso(heartbeat_at)
    age = (now - last).total_seconds()
    stale = age > stale_seconds
    return {"stale": stale, "age_seconds": age, "stale_seconds": stale_seconds, "status": "stale" if stale else "fresh"}


def heartbeat_policy() -> dict:
    return {"stale_seconds": 300, "crash_after_stale_seconds": 900, "heartbeat_required": True}
