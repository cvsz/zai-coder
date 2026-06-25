"""Tenant-aware gateway context."""

from __future__ import annotations

from dataclasses import dataclass

from .models import GatewayRequest


@dataclass(frozen=True)
class GatewayTenantContext:
    org_id: str
    workspace_id: str
    actor: str = "anonymous"
    source: str = "headers"

    def to_dict(self) -> dict:
        return self.__dict__.copy()


def extract_tenant_context(request: GatewayRequest) -> GatewayTenantContext | None:
    headers = {key.lower(): value for key, value in request.headers.items()}
    org_id = headers.get("x-org-id") or request.query.get("org_id")
    workspace_id = headers.get("x-workspace-id") or request.query.get("workspace_id")
    actor = headers.get("x-actor") or "anonymous"
    if not org_id or not workspace_id:
        return None
    return GatewayTenantContext(org_id=org_id, workspace_id=workspace_id, actor=actor)


def require_tenant_context(request: GatewayRequest) -> dict:
    context = extract_tenant_context(request)
    if context is None:
        return {"allowed": False, "reason": "missing tenant context"}
    return {"allowed": True, "context": context.to_dict()}
