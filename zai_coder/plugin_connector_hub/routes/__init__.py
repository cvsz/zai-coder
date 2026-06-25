"""Plugin Connector Hub route registry."""

from __future__ import annotations

import json
from pathlib import Path

from zai_coder.plugin_connector_hub.control import connector_hub_status, connector_hub_overview, install_connector_demo, enable_connector_demo
from zai_coder.plugin_connector_hub.catalog import connector_catalog, search_connectors, find_connector
from zai_coder.plugin_connector_hub.validator import validate_connector_manifest_payload, connector_security_report
from zai_coder.plugin_connector_hub.env_guard import validate_connector_env, redact_env
from zai_coder.plugin_connector_hub.permissions import connector_permission_decision
from zai_coder.plugin_connector_hub.install_policy import install_policy_decision, enable_policy_decision
from zai_coder.plugin_connector_hub.adapters import github_repo_plan, google_drive_index_plan, slack_summary_plan, cloudflare_access_plan, connector_status_plan
from zai_coder.plugin_connector_hub.sync import connector_sync_plan, sync_schedule_policy
from zai_coder.plugin_connector_hub.webhooks import webhook_ingress_draft, webhook_policy, sign_webhook_payload, verify_webhook_payload
from zai_coder.plugin_connector_hub.store import ConnectorStore
from zai_coder.plugin_connector_hub.import_export import export_connector_bundle, validate_connector_bundle
from zai_coder.plugin_connector_hub.ui.pages import render_connector_overview, render_connector_catalog_page, render_connector_policy_page, render_connector_sync_page


def route_connector_status() -> dict:
    return {
        "ok": True,
        "service": "zai-plugin-connector-hub",
        "systems": [
            "connector_catalog",
            "connector_manifest_validator",
            "env_secret_guard",
            "tenant_scoped_connector_permissions",
            "install_enable_policy",
            "dry_run_sync_plans",
            "webhook_ingress_scaffold",
            "provider_adapter_stubs",
            "connector_dashboard",
            "connector_audit_log",
        ],
    }


def route_connector_hub_overview() -> dict:
    return connector_hub_overview()


def route_connector_catalog() -> dict:
    return {"connectors": connector_catalog()}


def route_connector_search(query: str = "cloud") -> dict:
    return search_connectors(query)


def route_connector_validate_demo() -> dict:
    return validate_connector_manifest_payload(find_connector("github").to_dict())


def route_connector_security_report(connector_id: str = "github") -> dict:
    return connector_security_report(find_connector(connector_id))


def route_connector_env_check(connector_id: str = "github") -> dict:
    connector = find_connector(connector_id)
    return validate_connector_env(connector.required_env, {})


def route_connector_permission_decision() -> dict:
    return connector_permission_decision(("tenant_admin",), ("connector:view", "connector:install"))


def route_connector_install_policy(connector_id: str = "github") -> dict:
    return install_policy_decision(connector_id, ("tenant_admin",), {}, True, "", False)


def route_connector_enable_policy(connector_id: str = "github") -> dict:
    return enable_policy_decision(connector_id, ("tenant_admin",), {"GITHUB_TOKEN": "sandbox-token"}, "approved_manual_001")


def route_connector_install_demo() -> dict:
    return install_connector_demo()


def route_connector_enable_demo() -> dict:
    return enable_connector_demo()


def route_connector_adapter_plans() -> dict:
    return {
        "github": github_repo_plan(),
        "google_drive": google_drive_index_plan(),
        "slack": slack_summary_plan(),
        "cloudflare": cloudflare_access_plan(),
    }


def route_connector_sync_plan(connector_id: str = "github") -> dict:
    return connector_sync_plan(connector_id, action="status").to_dict()


def route_connector_sync_policy() -> dict:
    return sync_schedule_policy()


def route_connector_webhook_draft(connector_id: str = "github") -> dict:
    draft = webhook_ingress_draft(connector_id)
    payload = {"connector_id": connector_id, "event_type": draft.event_type}
    signature = sign_webhook_payload(payload)
    return {"draft": draft.to_dict(), "policy": webhook_policy(), "verification": verify_webhook_payload(payload, signature)}


def route_connector_audit() -> dict:
    return {"events": ConnectorStore().list_audit("org_local")}


def route_connector_export() -> dict:
    return {"path": export_connector_bundle(".")}


def route_connector_import_validate() -> dict:
    payload = {"kind": "zai-connector-bundle", "version": "1.0", "offline": True, "connectors": connector_catalog()}
    return validate_connector_bundle(payload)


def route_connector_page() -> dict:
    return {"content_type": "text/html", "html": render_connector_overview()}


def route_connector_catalog_page() -> dict:
    return {"content_type": "text/html", "html": render_connector_catalog_page()}


def route_connector_policy_page() -> dict:
    return {"content_type": "text/html", "html": render_connector_policy_page()}


def route_connector_sync_page() -> dict:
    return {"content_type": "text/html", "html": render_connector_sync_page()}
