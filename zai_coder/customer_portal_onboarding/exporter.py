"""Customer portal export helpers."""

from __future__ import annotations

import json
from pathlib import Path

from .accounts import customer_directory
from .features import feature_catalog
from .onboarding import onboarding_steps
from .workspace_setup import workspace_setup_plan


def redacted_customer(customer: dict) -> dict:
    row = dict(customer)
    if "owner_email" in row:
        name, _, domain = row["owner_email"].partition("@")
        row["owner_email"] = (name[:2] + "***@" + domain) if domain else "<redacted>"
    return row


def customer_export_bundle() -> dict:
    return {
        "kind": "zai-customer-portal-export",
        "version": "1.0",
        "customers": [redacted_customer(customer) for customer in customer_directory()],
        "features": feature_catalog(),
        "onboarding_steps": onboarding_steps(),
        "workspace_setup": workspace_setup_plan(),
        "safe_export": True,
        "external_publish": False,
    }


def write_customer_export(root: str | Path = ".", out: str = "customer/exports/customer-portal-export.json") -> str:
    root = Path(root)
    path = root / out
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(customer_export_bundle(), indent=2, sort_keys=True), encoding="utf-8")
    return str(path)
