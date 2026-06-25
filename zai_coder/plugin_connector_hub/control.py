"""Connector hub control helpers."""

from __future__ import annotations

from .catalog import connector_catalog, search_connectors
from .install_policy import install_policy_decision, enable_policy_decision
from .store import ConnectorStore


def connector_hub_status() -> dict:
    return {
        "ok": True,
        "systems": [
            "connector_catalog",
            "connector_manifest_validator",
            "env_secret_guard",
            "tenant_connector_permissions",
            "install_enable_policy",
            "dry_run_sync_plans",
            "webhook_ingress_scaffold",
            "provider_adapter_stubs",
            "connector_audit_log",
            "offline_import_export",
        ],
    }


def install_connector_demo(db_path: str = "data/plugin-connector-hub.db") -> dict:
    policy = install_policy_decision("github", ("tenant_admin",), {}, True, "", False)
    if not policy["allowed"]:
        return {"ok": False, "policy": policy}
    store = ConnectorStore(db_path)
    installation = store.install_connector("github", "org_local", "ws_default", "admin", False)
    audit = store.audit("org_local", "ws_default", "admin", "connector.installed", "github", installation.to_dict())
    return {"ok": True, "installation": installation.to_dict(), "audit": audit.to_dict()}


def enable_connector_demo(db_path: str = "data/plugin-connector-hub.db") -> dict:
    env = {"GITHUB_TOKEN": "sandbox-token"}
    policy = enable_policy_decision("github", ("tenant_admin",), env, "approved_manual_001")
    if not policy["allowed"]:
        return {"ok": False, "policy": policy}
    store = ConnectorStore(db_path)
    installation = store.install_connector("github", "org_local", "ws_default", "admin", False)
    store.set_enabled(installation.id, True)
    audit = store.audit("org_local", "ws_default", "admin", "connector.enabled", "github", {"installation_id": installation.id})
    return {"ok": True, "installation_id": installation.id, "audit": audit.to_dict()}


def connector_hub_overview() -> dict:
    return {"connectors": connector_catalog(), "search_demo": search_connectors("cloud")}
