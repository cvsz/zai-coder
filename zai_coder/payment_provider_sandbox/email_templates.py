"""Billing email templates."""

from __future__ import annotations


def billing_email_template(kind: str, org_name: str = "Local Org", plan_name: str = "Pro") -> dict:
    templates = {
        "checkout_created": {
            "subject": f"Sandbox checkout created for {org_name}",
            "body": f"A sandbox checkout draft was created for the {plan_name} plan. No real charge was made.",
        },
        "subscription_updated": {
            "subject": f"Subscription updated for {org_name}",
            "body": f"Your sandbox subscription is now associated with the {plan_name} plan.",
        },
        "payment_failed": {
            "subject": f"Sandbox payment failed for {org_name}",
            "body": "This is a sandbox payment failure notice. No real payment was attempted.",
        },
    }
    if kind not in templates:
        raise ValueError(f"unknown email template: {kind}")
    return {"kind": kind, **templates[kind], "safe_mode": True}


def billing_email_manifest() -> list[str]:
    return ["checkout_created", "subscription_updated", "payment_failed"]
