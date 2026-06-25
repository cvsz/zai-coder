"""Tenant-scoped audit helpers."""

from __future__ import annotations

import uuid

from .models import TenantAuditEvent, TenantPrincipal


def build_tenant_audit_event(principal: TenantPrincipal, action: str, target: str, payload: dict | None = None) -> TenantAuditEvent:
    return TenantAuditEvent(
        id=f"tae_{uuid.uuid4().hex[:12]}",
        org_id=principal.org_id,
        workspace_id=principal.workspace_id,
        actor=principal.actor,
        action=action,
        target=target,
        payload=payload or {},
    )


def audit_scope_filter(events: list[dict], org_id: str, workspace_id: str | None = None) -> list[dict]:
    filtered = [event for event in events if event.get("org_id") == org_id]
    if workspace_id:
        filtered = [event for event in filtered if event.get("workspace_id") == workspace_id]
    return filtered
