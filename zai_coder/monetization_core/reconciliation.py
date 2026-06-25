"""Reconciliation helpers for local monetization data."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List

from .ledger import CreditLedger
from .usage import UsageStore


@dataclass
class ReconciliationResult:
    account_id: str
    ledger_balance: int
    usage_units: int
    issues: List[str]

    def to_dict(self) -> dict:
        return {
            "account_id": self.account_id,
            "ledger_balance": self.ledger_balance,
            "usage_units": self.usage_units,
            "issues": list(self.issues),
        }


def reconcile_account(ledger: CreditLedger, usage: UsageStore, account_id: str, usage_resource: str = "credit_unit") -> ReconciliationResult:
    balance = ledger.balance(account_id)
    used = usage.total(account_id, usage_resource)
    issues: list[str] = []
    if balance < 0:
        issues.append("ledger balance is negative")
    if used < 0:
        issues.append("usage total is negative")
    return ReconciliationResult(account_id=account_id, ledger_balance=balance, usage_units=used, issues=issues)
