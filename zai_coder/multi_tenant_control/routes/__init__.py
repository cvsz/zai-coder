"""Multi-tenant control route registry."""

from __future__ import annotations

from zai_coder.core.booleans import coerce_bool
from zai_coder.multi_tenant_control.models import TenantPrincipal, WorkspaceQuota
from zai_coder.multi_tenant_control.store import TenantStore
from zai_coder.multi_tenant_control.api_keys import TenantApiKeyStore
from zai_coder.multi_tenant_control.isolation import cross_tenant_access_guard
from zai_coder.multi_tenant_control.quotas import quota_decision, default_usage
from zai_coder.multi_tenant_control.audit import build_tenant_audit_event
from zai_coder.multi_tenant_control.provider_permissions import provider_permission_decision
from zai_coder.multi_tenant_control.backup_export import tenant_backup_policy
from zai_coder.multi_tenant_control.onboarding import tenant_onboarding_plan
from zai_coder.multi_tenant_control.migration import tenant_migration_plan
from zai_coder.multi_tenant_control.ui.pages import render_tenant_overview, render_onboarding_page, render_backup_page, render_migration_page


def route_tenant_status() -> dict:
    return {
        "ok": True,
        "service": "zai-multi-tenant-control",
        "systems": [
            "tenant_org_workspace_runtime_isolation",
            "tenant_scoped_api_keys",
            "tenant_scoped_audit_logs",
            "workspace_quota_enforcement",
            "per_tenant_provider_permissions",
            "tenant_backup_export_policy",
            "tenant_onboarding_wizard",
            "admin_tenant_dashboard",
            "cross_tenant_access_guard",
            "tenant_migration_plan",
        ],
    }


def route_tenant_onboarding_plan() -> dict:
    return tenant_onboarding_plan()


def route_tenant_backup_policy() -> dict:
    return tenant_backup_policy()


def route_tenant_migration_plan() -> dict:
    return tenant_migration_plan()


def route_tenant_isolation_check(payload: dict | None = None) -> dict:
    payload = payload or {}
    principal = TenantPrincipal(
        actor=payload.get("actor", "admin"),
        org_id=payload.get("org_id", "org_local"),
        workspace_id=payload.get("workspace_id", "ws_default"),
        roles=tuple(payload.get("roles", ["tenant_admin"])),
    )
    return cross_tenant_access_guard(
        principal,
        payload.get("target_org_id", principal.org_id),
        payload.get("target_workspace_id", principal.workspace_id),
        payload.get("permission", "workspace:view"),
    )


def route_quota_decision(payload: dict | None = None) -> dict:
    payload = payload or {}
    quota = WorkspaceQuota(
        org_id=payload.get("org_id", "org_local"),
        workspace_id=payload.get("workspace_id", "ws_default"),
        monthly_runs_limit=int(payload.get("monthly_runs_limit", 1000)),
        storage_mb_limit=int(payload.get("storage_mb_limit", 1024)),
        provider_apply_limit=int(payload.get("provider_apply_limit", 100)),
    )
    return quota_decision(quota, payload.get("usage", default_usage()))


def route_provider_permission(payload: dict | None = None) -> dict:
    payload = payload or {}
    principal = TenantPrincipal(
        actor=payload.get("actor", "admin"),
        org_id=payload.get("org_id", "org_local"),
        workspace_id=payload.get("workspace_id", "ws_default"),
        roles=tuple(payload.get("roles", ["tenant_admin"])),
    )
    return provider_permission_decision(principal, payload.get("provider", "github"), coerce_bool(payload.get("apply", False)))


def route_create_tenant_demo() -> dict:
    store = TenantStore()
    org = store.create_org("Local Org", f"local-org-demo")
    ws = store.create_workspace(org.id, "Default", "default")
    principal = store.add_membership(TenantPrincipal("admin", org.id, ws.id, ("tenant_owner",)))
    event = store.record_audit(build_tenant_audit_event(principal, "tenant.created", org.id))
    return {"org": org.to_dict(), "workspace": ws.to_dict(), "principal": principal.to_dict(), "audit": event.to_dict()}


def route_create_tenant_api_key(payload: dict | None = None) -> dict:
    payload = payload or {}
    key, token = TenantApiKeyStore().create_key(
        payload.get("org_id", "org_local"),
        payload.get("workspace_id", "ws_default"),
        payload.get("name", "default"),
        tuple(payload.get("scopes", ["workspace:view"])),
    )
    return {"key": key.to_public_dict(), "token_preview": token[:18] + "..."}


def route_tenant_page() -> dict:
    return {"content_type": "text/html", "html": render_tenant_overview()}


def route_tenant_onboarding_page() -> dict:
    return {"content_type": "text/html", "html": render_onboarding_page()}


def route_tenant_backup_page() -> dict:
    return {"content_type": "text/html", "html": render_backup_page()}


def route_tenant_migration_page() -> dict:
    return {"content_type": "text/html", "html": render_migration_page()}
