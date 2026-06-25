"""Tenant-scoped worker guard."""

from __future__ import annotations


def tenant_worker_guard(worker: dict, job: dict) -> dict:
    scope = worker.get("tenant_scope", "shared")
    if scope == "shared":
        return {"allowed": True, "reason": "shared worker"}
    expected = f"{job.get('org_id')}:{job.get('workspace_id')}"
    if scope != expected:
        return {"allowed": False, "reason": "worker tenant scope mismatch", "expected": expected, "actual": scope}
    return {"allowed": True, "reason": "tenant scope matched"}


def tenant_worker_scope(org_id: str, workspace_id: str) -> str:
    if not org_id or not workspace_id:
        raise ValueError("org_id and workspace_id required")
    return f"{org_id}:{workspace_id}"
