from pathlib import Path
import tempfile

from zai_coder.production_api_gateway.models import GatewayRequest, GatewayRoute, UpstreamService
from zai_coder.production_api_gateway.envelope import success_response, error_response
from zai_coder.production_api_gateway.headers import security_headers, cors_headers, gateway_headers
from zai_coder.production_api_gateway.tenant_context import extract_tenant_context, require_tenant_context
from zai_coder.production_api_gateway.auth import extract_auth_token, auth_decision
from zai_coder.production_api_gateway.rate_limit import InMemoryRateLimiter, rate_limit_policy_manifest
from zai_coder.production_api_gateway.upstreams import upstream_manifest, get_upstream, upstream_health_plan
from zai_coder.production_api_gateway.router import route_manifest, find_route, GatewayDispatcher
from zai_coder.production_api_gateway.request_validation import validate_gateway_request
from zai_coder.production_api_gateway.audit import GatewayAuditLog
from zai_coder.production_api_gateway.openapi import gateway_openapi_schema
from zai_coder.production_api_gateway.deploy import gateway_deploy_plan, gateway_smoke_plan
from zai_coder.production_api_gateway.ui.pages import render_gateway_overview, render_routes_page, render_upstreams_page, render_security_page
from zai_coder.production_api_gateway.routes import (
    route_gateway_status,
    route_gateway_routes,
    route_gateway_upstreams,
    route_gateway_headers,
    route_gateway_rate_limits,
    route_gateway_openapi,
    route_gateway_deploy_plan,
    route_gateway_smoke_plan,
    route_gateway_dispatch_demo,
    route_gateway_protected_demo,
    route_gateway_audit,
    route_gateway_page,
    route_gateway_routes_page,
    route_gateway_upstreams_page,
    route_gateway_security_page,
)


def test_models_validation_and_safe_request():
    req = GatewayRequest("get", "/api/test", headers={"Authorization": "Bearer secret", "X-Org-Id": "org"})
    safe = req.to_safe_dict()
    assert safe["headers"]["Authorization"] == "<redacted>"
    assert GatewayRoute("r", "GET", "/x", "core").validate() == []
    assert GatewayRoute("r", "BAD", "x", "").validate()
    assert UpstreamService("u", "U", "http://127.0.0.1:9999").validate() == []
    assert UpstreamService("u", "U", "https://example.com").validate()


def test_envelope_headers_auth_tenant():
    ok = success_response({"hello": "world"})
    err = error_response("bad", "message", 400)
    assert ok.body["ok"] is True
    assert err.body["ok"] is False
    assert "X-Frame-Options" in security_headers()
    assert cors_headers("https://evil.example")["Access-Control-Allow-Origin"] == "http://127.0.0.1:8765"
    assert "Cache-Control" in gateway_headers()
    req = GatewayRequest("GET", "/x", headers={"Authorization": "Bearer abcdefghijkl", "X-Org-Id": "org", "X-Workspace-Id": "ws"})
    assert extract_auth_token(req) == "abcdefghijkl"
    assert auth_decision(req)["allowed"] is True
    assert extract_tenant_context(req).org_id == "org"
    assert require_tenant_context(req)["allowed"] is True
    assert require_tenant_context(GatewayRequest("GET", "/x"))["allowed"] is False


def test_rate_limits_upstreams_routes():
    limiter = InMemoryRateLimiter()
    assert limiter.check("id", "standard")["allowed"] is True
    assert rate_limit_policy_manifest()
    assert upstream_manifest()
    assert get_upstream("core").id == "core"
    assert upstream_health_plan()["dry_run"] is True
    assert route_manifest()
    assert find_route("GET", "/api/gateway/status").id == "status"
    assert find_route("POST", "/missing") is None


def test_dispatcher_behaviors():
    dispatcher = GatewayDispatcher()
    public_req = GatewayRequest("GET", "/api/gateway/status")
    response = dispatcher.dispatch(public_req)
    assert response.status == 200
    missing = dispatcher.dispatch(GatewayRequest("GET", "/missing"))
    assert missing.status == 404
    protected_no_auth = dispatcher.dispatch(GatewayRequest("GET", "/api/tenants/status"))
    assert protected_no_auth.status == 401
    protected_no_tenant = dispatcher.dispatch(GatewayRequest("GET", "/api/tenants/status", headers={"Authorization": "Bearer abcdefghijkl"}))
    assert protected_no_tenant.status == 400
    protected_ok = dispatcher.dispatch(GatewayRequest("GET", "/api/tenants/status", headers={"Authorization": "Bearer abcdefghijkl", "X-Org-Id": "org", "X-Workspace-Id": "ws"}))
    assert protected_ok.status == 200


def test_request_validation_audit_openapi_deploy(tmp_path):
    assert validate_gateway_request(GatewayRequest("GET", "/x"))["ok"] is True
    assert validate_gateway_request(GatewayRequest("BAD", "x"))["ok"] is False
    audit = GatewayAuditLog(tmp_path / "gateway-audit.db")
    req = GatewayRequest("GET", "/api/gateway/status", headers={"X-Org-Id": "org", "X-Workspace-Id": "ws", "X-Actor": "admin"})
    res = success_response({"ok": True})
    event = audit.record(req, res)
    assert audit.list_events()[0]["id"] == event.id
    schema = gateway_openapi_schema()
    assert schema["info"]["version"] == "v24"
    assert "/api/gateway/status" in schema["paths"]
    assert gateway_deploy_plan()["dry_run"] is True
    assert gateway_smoke_plan()["dry_run"] is True


def test_ui_pages():
    assert "Production API Gateway" in render_gateway_overview()
    assert "Gateway Routes" in render_routes_page()
    assert "Upstreams" in render_upstreams_page()
    assert "Gateway Security" in render_security_page()


def test_routes(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    assert route_gateway_status()["ok"] is True
    assert route_gateway_routes()["routes"]
    assert route_gateway_upstreams()["upstreams"]
    assert "headers" in route_gateway_headers()
    assert route_gateway_rate_limits()["policies"]
    assert route_gateway_openapi()["info"]["title"]
    assert route_gateway_deploy_plan()["dry_run"] is True
    assert route_gateway_smoke_plan()["dry_run"] is True
    assert route_gateway_dispatch_demo()["response"]["status"] == 200
    assert route_gateway_protected_demo()["status"] == 200
    assert "events" in route_gateway_audit()
    assert route_gateway_page()["content_type"] == "text/html"
    assert route_gateway_routes_page()["content_type"] == "text/html"
    assert route_gateway_upstreams_page()["content_type"] == "text/html"
    assert route_gateway_security_page()["content_type"] == "text/html"


def test_docs_scripts_assets_exist():
    root = Path(__file__).resolve().parents[1]
    for rel in [
        "scripts/gateway/gateway-status.sh",
        "scripts/gateway/gateway-routes.sh",
        "scripts/gateway/gateway-upstreams.sh",
        "scripts/gateway/gateway-headers.sh",
        "scripts/gateway/gateway-openapi-export.sh",
        "scripts/gateway/gateway-dispatch-demo.sh",
        "scripts/gateway/gateway-audit.sh",
        "scripts/gateway/gateway-deploy-plan.sh",
        "scripts/gateway/gateway-dashboard-export.sh",
        "deploy/gateway/gateway.example.env",
        "docs/gateway/PRODUCTION_API_GATEWAY_GUIDE.md",
        "docs/gateway/GATEWAY_SECURITY.md",
        "docs/gateway/GATEWAY_ROUTES.md",
        "docs/gateway/GATEWAY_UPSTREAMS.md",
        "docs/gateway/GATEWAY_DEPLOYMENT.md",
        "docs/requirements/NEXT_V24_PRODUCTION_API_GATEWAY_REQUIREMENTS.md",
        "assets/gateway/production_api_gateway_features.json",
    ]:
        assert (root / rel).exists(), rel
