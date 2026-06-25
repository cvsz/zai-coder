import tempfile
from pathlib import Path
import zipfile

from zai_coder.app_studio_final.ui.shell import render_shell
from zai_coder.app_studio_final.ui.pages import render_home_page, render_plugins_page, render_workflows_page, render_models_page, render_deployments_page
from zai_coder.app_studio_final.plugin_marketplace import list_plugins, get_plugin
from zai_coder.app_studio_final.wizards.app_generator import generate_app_plan
from zai_coder.app_studio_final.workflow_builder import default_release_workflow, WorkflowStep, Workflow
from zai_coder.app_studio_final.model_router_ui import list_model_routes
from zai_coder.app_studio_final.deployment_control import default_deployment_targets
from zai_coder.app_studio_final.api_key_ui import render_api_keys_page
from zai_coder.app_studio_final.audit_search import search_audit_events
from zai_coder.app_studio_final.approval_queue import ApprovalQueue
from zai_coder.app_studio_final.project_archive import export_project_archive, inspect_project_archive
from zai_coder.app_studio_final.routes import (
    route_final_status,
    route_home,
    route_plugins,
    route_workflows,
    route_models,
    route_deployments,
    route_app_generator,
    route_audit_search,
)
from zai_coder.app_studio_final.openapi_full import build_full_openapi_schema, export_full_openapi_json


def test_ui_pages_render():
    assert "ZAI App Studio" in render_shell("T", "<h1>X</h1>")
    assert "Control Center" in render_home_page()
    assert "Plugin Marketplace" in render_plugins_page(list_plugins())
    assert "AI Workflow Builder" in render_workflows_page([{"name":"W","status":"draft","steps":["a","b"]}])
    assert "Model Router" in render_models_page(list_model_routes())
    assert "Deployment Control Center" in render_deployments_page(default_deployment_targets())


def test_plugin_marketplace():
    plugins = list_plugins()
    assert len(plugins) >= 5
    assert get_plugin("github").name == "GitHub Publisher"


def test_app_generator():
    plan = generate_app_plan("Demo App", "web")
    assert plan.dry_run is True
    assert "apps/demo-app/README.md" in plan.files


def test_workflow_builder():
    wf = default_release_workflow()
    assert wf.validate() == []
    bad = Workflow("", "", [WorkflowStep("", "bad")])
    assert bad.validate()


def test_model_router_and_deployment_targets():
    assert list_model_routes()[0]["local_first"] is True
    targets = default_deployment_targets()
    assert any(t["target_type"] == "cloudflare" for t in targets)


def test_api_key_ui_and_audit_search():
    html = render_api_keys_page([{"name":"admin","prefix":"zai_abc","status":"active"}])
    assert "API Keys" in html
    events = [{"actor":"alice","action":"deploy","target":"cloudflare"}, {"actor":"bob","action":"test","target":"ci"}]
    assert len(search_audit_events(events, query="cloudflare")) == 1
    assert len(search_audit_events(events, actor="bob")) == 1


def test_approval_queue():
    with tempfile.TemporaryDirectory() as td:
        q = ApprovalQueue(Path(td) / "approval.db")
        item = q.submit("github", "release", {"dry_run": True}, "admin")
        assert item.status == "pending"
        q.decide(item.id, "approved")


def test_project_archive_export_import():
    with tempfile.TemporaryDirectory() as td:
        root = Path(td) / "project"
        root.mkdir()
        (root / "README.md").write_text("hello", encoding="utf-8")
        (root / ".env").write_text("SECRET=1", encoding="utf-8")
        archive = Path(td) / "project.zip"
        plan = export_project_archive(root, archive, {"name":"demo"}, apply=False)
        assert plan["dry_run"] is True
        real = export_project_archive(root, archive, {"name":"demo"}, apply=True)
        assert real["dry_run"] is False
        info = inspect_project_archive(archive)
        assert info["unsafe"] == []
        with zipfile.ZipFile(archive) as z:
            names = set(z.namelist())
        assert "README.md" in names
        assert ".env" not in names


def test_final_routes_and_openapi():
    assert route_final_status()["ok"] is True
    assert route_home()["content_type"] == "text/html"
    assert route_plugins()["content_type"] == "text/html"
    assert route_workflows()["content_type"] == "text/html"
    assert route_models()["content_type"] == "text/html"
    assert route_deployments()["content_type"] == "text/html"
    assert route_app_generator({"app_name":"Demo","app_type":"api"})["app_type"] == "api"
    assert len(route_audit_search({"events":[{"actor":"a","action":"x","target":"y"}], "query":"y"})["results"]) == 1
    schema = build_full_openapi_schema()
    assert schema["info"]["version"] == "0.12.0"
    assert "/api/final/status" in schema["paths"]
    assert "ZAI Coder App Studio Final API" in export_full_openapi_json()


def test_final_docs_scripts_exist():
    root = Path(__file__).resolve().parents[1]
    assert (root / "docs/final/FINAL_RELEASE_NOTES.md").exists()
    assert (root / "docs/final/END_PROJECT_CHECKLIST.md").exists()
    assert (root / "scripts/final/final-status.sh").exists()
    assert (root / "assets/app_studio_final_features.json").exists()
