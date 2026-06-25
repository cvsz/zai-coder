from pathlib import Path
import tempfile
import json

from zai_coder.plugin_connector_hub.models import ConnectorManifest, ConnectorInstallation, ConnectorSyncPlan, WebhookIngressDraft
from zai_coder.plugin_connector_hub.catalog import connector_catalog, find_connector, search_connectors
from zai_coder.plugin_connector_hub.validator import validate_connector_manifest_payload, connector_security_report
from zai_coder.plugin_connector_hub.env_guard import redact_env, validate_connector_env
from zai_coder.plugin_connector_hub.permissions import permissions_for_roles, connector_permission_decision
from zai_coder.plugin_connector_hub.install_policy import install_policy_decision, enable_policy_decision
from zai_coder.plugin_connector_hub.adapters import github_repo_plan, google_drive_index_plan, slack_summary_plan, cloudflare_access_plan, connector_action_plan
from zai_coder.plugin_connector_hub.sync import connector_sync_plan, sync_schedule_policy
from zai_coder.plugin_connector_hub.webhooks import sign_webhook_payload, verify_webhook_payload, webhook_ingress_draft, webhook_policy
from zai_coder.plugin_connector_hub.store import ConnectorStore
from zai_coder.plugin_connector_hub.import_export import export_connector_bundle, validate_connector_bundle
from zai_coder.plugin_connector_hub.control import connector_hub_status, install_connector_demo, enable_connector_demo, connector_hub_overview
from zai_coder.plugin_connector_hub.ui.pages import render_connector_overview, render_connector_catalog_page, render_connector_policy_page, render_connector_sync_page
from zai_coder.plugin_connector_hub.routes import (
    route_connector_status,
    route_connector_hub_overview,
    route_connector_catalog,
    route_connector_search,
    route_connector_validate_demo,
    route_connector_security_report,
    route_connector_env_check,
    route_connector_permission_decision,
    route_connector_install_policy,
    route_connector_enable_policy,
    route_connector_install_demo,
    route_connector_enable_demo,
    route_connector_adapter_plans,
    route_connector_sync_plan,
    route_connector_sync_policy,
    route_connector_webhook_draft,
    route_connector_audit,
    route_connector_export,
    route_connector_import_validate,
    route_connector_page,
    route_connector_catalog_page,
    route_connector_policy_page,
    route_connector_sync_page,
)


def test_models_validation():
    assert ConnectorManifest("c", "Connector", "provider", "1.0.0", "desc").validate() == []
    assert ConnectorManifest("../bad", "", "", "", "desc", required_env=("LIVE_SECRET",)).validate()
    assert ConnectorInstallation("i", "c", "org", "ws").validate() == []
    assert ConnectorInstallation("", "", "", "").validate()
    assert ConnectorSyncPlan("s", "c", "org", "ws", "status").validate() == []
    assert ConnectorSyncPlan("", "", "", "", "", dry_run=False).validate()
    assert WebhookIngressDraft("w", "github", "event", "org", "ws", secret_env="GITHUB_WEBHOOK_SECRET").validate() == []


def test_catalog_validator_env_permissions_policy():
    assert connector_catalog()
    assert find_connector("github").provider == "github"
    assert search_connectors("cloud")["connectors"]
    payload = find_connector("github").to_dict()
    assert validate_connector_manifest_payload(payload)["ok"] is True
    risky = ConnectorManifest("r", "Risky", "risky", "1.0.0", "desc", required_permissions=("providers:apply",))
    assert connector_security_report(risky)["ok"] is False
    assert redact_env({"GITHUB_TOKEN": "secret", "SAFE": "ok"})["GITHUB_TOKEN"] == "<redacted>"
    assert validate_connector_env(("GITHUB_TOKEN",), {"GITHUB_TOKEN": "x"})["ok"] is True
    assert validate_connector_env(("GITHUB_TOKEN",), {})["ok"] is False
    assert "connector:install" in permissions_for_roles(("tenant_admin",))
    assert connector_permission_decision(("viewer",), ("connector:view",))["allowed"] is True
    assert connector_permission_decision(("viewer",), ("connector:install",))["allowed"] is False
    assert install_policy_decision("github")["allowed"] is True
    assert install_policy_decision("github", dry_run_completed=False)["allowed"] is False
    assert enable_policy_decision("github", env={"GITHUB_TOKEN": "x"})["allowed"] is True
    assert enable_policy_decision("github", env={})["allowed"] is False


def test_adapters_sync_webhooks():
    assert github_repo_plan()["dry_run"] is True
    assert google_drive_index_plan()["dry_run"] is True
    assert slack_summary_plan()["dry_run"] is True
    assert cloudflare_access_plan()["dry_run"] is True
    try:
        connector_action_plan("github", "bad-action")
        assert False
    except ValueError:
        assert True
    sync = connector_sync_plan("github", action="status")
    assert sync.dry_run is True
    assert sync_schedule_policy()["external_calls_disabled_by_default"] is True
    payload = {"event": "x"}
    sig = sign_webhook_payload(payload)
    assert verify_webhook_payload(payload, sig)["ok"] is True
    draft = webhook_ingress_draft("github")
    assert draft.secret_env == "GITHUB_WEBHOOK_SECRET"
    assert webhook_policy()["requires_signature"] is True


def test_store_import_export_control(tmp_path):
    store = ConnectorStore(tmp_path / "connectors.db")
    inst = store.install_connector("github", "org", "ws", "admin", False)
    assert inst.id.startswith("cinst_")
    store.set_enabled(inst.id, True)
    assert store.list_installations("org", "ws")[0]["enabled"] is True
    event = store.audit("org", "ws", "admin", "connector.installed", "github")
    assert store.list_audit("org")[0]["id"] == event.id
    bundle_path = export_connector_bundle(tmp_path)
    payload = json.loads(Path(bundle_path).read_text())
    assert validate_connector_bundle(payload)["ok"] is True
    assert connector_hub_status()["ok"] is True
    assert install_connector_demo(str(tmp_path / "hub2.db"))["ok"] is True
    assert enable_connector_demo(str(tmp_path / "hub3.db"))["ok"] is True
    assert connector_hub_overview()["connectors"]


def test_ui_pages():
    assert "Plugin Connector Hub" in render_connector_overview()
    assert "Connector Catalog" in render_connector_catalog_page()
    assert "Connector Policy" in render_connector_policy_page()
    assert "Connector Sync" in render_connector_sync_page()


def test_routes(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    assert route_connector_status()["ok"] is True
    assert route_connector_hub_overview()["connectors"]
    assert route_connector_catalog()["connectors"]
    assert route_connector_search("cloud")["connectors"]
    assert route_connector_validate_demo()["ok"] is True
    assert route_connector_security_report("github")["ok"] is False  # webhook connector lacks declared webhook secret in catalog
    assert route_connector_env_check("github")["ok"] is False
    assert route_connector_permission_decision()["allowed"] is True
    assert route_connector_install_policy("github")["allowed"] is True
    assert route_connector_enable_policy("github")["allowed"] is True
    assert route_connector_install_demo()["ok"] is True
    assert route_connector_enable_demo()["ok"] is True
    assert route_connector_adapter_plans()["github"]["dry_run"] is True
    assert route_connector_sync_plan("github")["dry_run"] is True
    assert route_connector_sync_policy()["dry_run"] is True
    assert route_connector_webhook_draft("github")["verification"]["ok"] is True
    assert "events" in route_connector_audit()
    assert Path(route_connector_export()["path"]).exists()
    assert route_connector_import_validate()["ok"] is True
    assert route_connector_page()["content_type"] == "text/html"
    assert route_connector_catalog_page()["content_type"] == "text/html"
    assert route_connector_policy_page()["content_type"] == "text/html"
    assert route_connector_sync_page()["content_type"] == "text/html"


def test_docs_scripts_assets_exist():
    root = Path(__file__).resolve().parents[1]
    for rel in [
        "scripts/connectors/connector-status.sh",
        "scripts/connectors/connector-catalog.sh",
        "scripts/connectors/connector-search.sh",
        "scripts/connectors/connector-validate.sh",
        "scripts/connectors/connector-env-check.sh",
        "scripts/connectors/connector-install-policy.sh",
        "scripts/connectors/connector-install-demo.sh",
        "scripts/connectors/connector-enable-demo.sh",
        "scripts/connectors/connector-adapter-plans.sh",
        "scripts/connectors/connector-sync-plan.sh",
        "scripts/connectors/connector-webhook-draft.sh",
        "scripts/connectors/connector-audit.sh",
        "scripts/connectors/connector-export.sh",
        "scripts/connectors/connector-dashboard-export.sh",
        "docs/connectors/PLUGIN_CONNECTOR_HUB_GUIDE.md",
        "docs/connectors/CONNECTOR_MANIFEST.md",
        "docs/connectors/CONNECTOR_INSTALL_POLICY.md",
        "docs/connectors/CONNECTOR_ENV_SECRET_GUARD.md",
        "docs/connectors/CONNECTOR_WEBHOOKS.md",
        "docs/connectors/CONNECTOR_ADAPTERS.md",
        "docs/requirements/NEXT_V28_PLUGIN_CONNECTOR_HUB_REQUIREMENTS.md",
        "assets/connectors/plugin_connector_hub_features.json",
    ]:
        assert (root / rel).exists(), rel
