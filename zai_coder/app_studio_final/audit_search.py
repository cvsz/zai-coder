"""Audit search model."""

from __future__ import annotations


def search_audit_events(events: list[dict], query: str = "", actor: str = "", action: str = "") -> list[dict]:
    q = query.lower().strip()
    results = []
    for event in events:
        if actor and event.get("actor") != actor:
            continue
        if action and event.get("action") != action:
            continue
        blob = " ".join(str(v) for v in event.values()).lower()
        if q and q not in blob:
            continue
        results.append(event)
    return results
