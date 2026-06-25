"""Billing audit trail helpers."""

from __future__ import annotations

from .ledger import UsageLedger


def billing_audit_summary(org_id: str, ledger: UsageLedger | None = None) -> dict:
    ledger = ledger or UsageLedger()
    events = ledger.list_audit(org_id)
    by_action = {}
    for event in events:
        by_action[event["action"]] = by_action.get(event["action"], 0) + 1
    return {"org_id": org_id, "total": len(events), "by_action": by_action, "events": events}
