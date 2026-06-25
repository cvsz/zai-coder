"""Customer onboarding wizard."""

from __future__ import annotations

import uuid
import json
from pathlib import Path

from .models import OnboardingStep, OnboardingPlan
from .accounts import find_customer


DEFAULT_STEPS = [
    OnboardingStep("welcome", "Welcome and product orientation", "Review local-first platform overview.", "customer", True, "pending", 10),
    OnboardingStep("workspace", "Create default workspace", "Prepare tenant workspace setup plan.", "platform", True, "pending", 20),
    OnboardingStep("security", "Review security defaults", "Confirm RBAC, support access, and audit settings.", "customer", True, "pending", 30),
    OnboardingStep("billing", "Review billing mode", "Confirm draft-only billing and no-real-charge policy.", "billing", True, "pending", 40),
    OnboardingStep("connectors", "Plan connector setup", "Select connector plans without external provider calls.", "customer", False, "pending", 50),
    OnboardingStep("go-live", "Go-live readiness checklist", "Review health, rollback, and support workflow.", "support", True, "pending", 60),
]


def onboarding_steps() -> list[dict]:
    return [step.to_dict() for step in sorted(DEFAULT_STEPS, key=lambda step: step.order)]


def onboarding_step_validation_report() -> dict:
    reports = [{"id": step.id, "issues": step.validate()} for step in DEFAULT_STEPS]
    return {"ok": all(not item["issues"] for item in reports), "reports": reports}


def build_onboarding_plan(customer_id: str = "cust_demo", workspace_id: str = "ws_demo") -> OnboardingPlan:
    customer = find_customer(customer_id)
    plan = OnboardingPlan(
        id=f"onb_{uuid.uuid4().hex[:12]}",
        customer_id=customer.id,
        org_id=customer.org_id,
        workspace_id=workspace_id,
        steps=tuple(onboarding_steps()),
    )
    issues = plan.validate()
    if issues:
        raise ValueError("; ".join(issues))
    return plan


def onboarding_progress(plan_payload: dict) -> dict:
    steps = plan_payload["steps"]
    required = [step for step in steps if step["required"]]
    completed = [step for step in required if step["status"] == "completed"]
    percent = 100.0 if not required else round((len(completed) / len(required)) * 100, 2)
    blocked = [step for step in steps if step["status"] == "blocked"]
    return {
        "percent_complete": percent,
        "required_steps": len(required),
        "completed_required_steps": len(completed),
        "blocked_steps": blocked,
        "ready": percent == 100.0 and not blocked,
    }


def write_onboarding_plan(plan: OnboardingPlan, root: str | Path = ".", out_dir: str = "customer/onboarding") -> str:
    root = Path(root)
    path = root / out_dir / f"{plan.id}.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(plan.to_dict(), indent=2, sort_keys=True), encoding="utf-8")
    return str(path)
