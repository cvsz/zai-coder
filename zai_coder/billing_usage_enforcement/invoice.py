"""Invoice draft generator."""

from __future__ import annotations

import json
import uuid
from pathlib import Path

from .models import BillingAccount, InvoiceDraft, WorkspaceUsageSummary
from .plans import get_plan
from .overage import calculate_overage_cents


def generate_invoice_draft(account: BillingAccount, usage: WorkspaceUsageSummary) -> InvoiceDraft:
    issues = account.validate()
    if issues:
        raise ValueError("; ".join(issues))
    plan = get_plan(account.plan_id)
    overage = calculate_overage_cents(account.plan_id, usage)
    line_items = [
        {"description": f"{plan.name} monthly plan", "amount_cents": plan.monthly_price_cents},
    ]
    for key, amount in overage["charges_cents"].items():
        if amount:
            line_items.append({"description": f"{key} overage", "amount_cents": amount})
    subtotal = plan.monthly_price_cents
    total = subtotal + overage["total_cents"]
    return InvoiceDraft(
        id=f"inv_{uuid.uuid4().hex[:12]}",
        org_id=account.org_id,
        plan_id=account.plan_id,
        currency=account.currency,
        subtotal_cents=subtotal,
        overage_cents=overage["total_cents"],
        total_cents=total,
        line_items=tuple(line_items),
    )


def write_invoice_draft(invoice: InvoiceDraft, root: str | Path = ".", out_dir: str = "invoices/drafts") -> str:
    root = Path(root)
    path = root / out_dir / f"{invoice.id}.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(invoice.to_dict(), indent=2, sort_keys=True), encoding="utf-8")
    return str(path)
