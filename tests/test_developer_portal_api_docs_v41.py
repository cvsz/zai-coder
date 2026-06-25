from pathlib import Path
from zai_coder.developer_portal_api_docs.models import ApiEndpoint, SdkSnippet, Quickstart
from zai_coder.developer_portal_api_docs.core import *
from zai_coder.developer_portal_api_docs.routes import *

def test_models_validation():
    assert ApiEndpoint("e","GET","/x","summary").validate() == []
    assert ApiEndpoint("","BAD","x","", stability="bad").validate()
    assert SdkSnippet("s","bash","Title","curl http://localhost","e").validate() == []
    assert SdkSnippet("","bad","","secret token_live","").validate()
    assert Quickstart("q","Title","developer",("step",)).validate() == []
    assert Quickstart("","","bad",(), status="bad").validate()

def test_core_docs():
    assert endpoint_registry()
    assert snippet_registry()
    assert quickstart_registry()
    assert validation_report()["ok"]
    spec = openapi_spec()
    assert spec["openapi"] == "3.1.0"
    assert "/api/team/status" in spec["paths"]
    assert docs_export_bundle()["external_publish"] is False

def test_exports(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    assert Path(write_openapi_export(tmp_path)).exists()
    assert Path(write_docs_export(tmp_path)).exists()
    assert Path(write_developer_report(tmp_path)).exists()
    demo = developer_demo(str(tmp_path))
    assert Path(demo["openapi_path"]).exists()
    assert Path(demo["export_path"]).exists()

def test_routes():
    assert route_developer_status()["ok"]
    assert route_developer_overview()["validation"]["ok"]
    assert route_api_reference()["validation"]["ok"]
    assert "openapi" in route_openapi_export()
    assert route_sdk_snippets()["snippets"]
    assert route_quickstarts()["quickstarts"]
    assert "export_path" in route_developer_docs_export()
    assert "openapi_path" in route_developer_demo()
    assert route_developer_page()["content_type"] == "text/html"
    assert route_developer_api_page()["content_type"] == "text/html"
    assert route_developer_openapi_page()["content_type"] == "text/html"
    assert route_developer_snippets_page()["content_type"] == "text/html"
    assert route_developer_quickstarts_page()["content_type"] == "text/html"

def test_docs_scripts_assets_exist():
    root = Path(__file__).resolve().parents[1]
    for rel in [
        "scripts/developer-portal/dev-portal-status.sh",
        "scripts/developer-portal/api-reference.sh",
        "scripts/developer-portal/openapi-export.sh",
        "scripts/developer-portal/sdk-snippets.sh",
        "scripts/developer-portal/integration-quickstarts.sh",
        "scripts/developer-portal/developer-docs-export.sh",
        "scripts/developer-portal/developer-demo.sh",
        "scripts/developer-portal/developer-portal-dashboard-export.sh",
        "docs/developer-portal/DEVELOPER_PORTAL_API_DOCS_GUIDE.md",
        "docs/developer-portal/API_REFERENCE.md",
        "docs/developer-portal/OPENAPI_EXPORT.md",
        "docs/developer-portal/SDK_SNIPPETS.md",
        "docs/requirements/NEXT_V41_DEVELOPER_PORTAL_API_DOCS_REQUIREMENTS.md",
        "assets/developer-portal/developer_portal_api_docs_features.json",
    ]:
        assert (root / rel).exists(), rel
