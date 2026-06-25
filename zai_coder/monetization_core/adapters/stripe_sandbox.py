"""Stripe sandbox adapter placeholder.

This adapter never makes live API calls. It only builds plans for future integration.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class CheckoutPlan:
    provider: str
    plan_slug: str
    account_id: str
    dry_run: bool = True
    warning: str = "Sandbox placeholder only. No payment API call was made."

    def to_dict(self) -> dict:
        return {
            "provider": self.provider,
            "plan_slug": self.plan_slug,
            "account_id": self.account_id,
            "dry_run": self.dry_run,
            "warning": self.warning,
        }


def create_checkout_plan(account_id: str, plan_slug: str) -> CheckoutPlan:
    if not account_id:
        raise ValueError("missing account_id")
    if not plan_slug:
        raise ValueError("missing plan_slug")
    return CheckoutPlan(provider="stripe_sandbox", account_id=account_id, plan_slug=plan_slug)
