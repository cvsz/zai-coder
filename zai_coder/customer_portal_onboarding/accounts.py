"""Customer account directory."""

from __future__ import annotations

import uuid

from .models import CustomerAccount


DEFAULT_CUSTOMERS = [
    CustomerAccount("cust_local", "org_local", "Local Customer", "owner@example.local", "internal", "active"),
    CustomerAccount("cust_demo", "org_demo", "Demo Customer", "demo@example.local", "free", "onboarding"),
]


def customer_directory() -> list[dict]:
    return [customer.to_dict() for customer in DEFAULT_CUSTOMERS]


def find_customer(customer_id: str) -> CustomerAccount:
    for customer in DEFAULT_CUSTOMERS:
        if customer.id == customer_id:
            return customer
    raise ValueError(f"unknown customer: {customer_id}")


def customer_validation_report() -> dict:
    reports = [{"id": customer.id, "issues": customer.validate()} for customer in DEFAULT_CUSTOMERS]
    return {"ok": all(not item["issues"] for item in reports), "reports": reports}


def create_customer_plan(name: str, owner_email: str, plan: str = "free", region: str = "global") -> dict:
    customer = CustomerAccount(f"cust_{uuid.uuid4().hex[:12]}", f"org_{uuid.uuid4().hex[:8]}", name, owner_email, plan, "onboarding", region)
    issues = customer.validate()
    return {
        "dry_run": True,
        "allowed": not issues,
        "issues": issues,
        "customer": customer.to_dict(),
        "provision": False,
        "send_email": False,
    }
