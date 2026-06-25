"""Production API Gateway route registry."""

from __future__ import annotations

from zai_coder.production_api_gateway.models import GatewayRequest
from zai_coder.production_api_gateway.router import GatewayDispatcher, route_manifest
from zai_coder.production_api_gateway.request_validation import validate_gateway_request
from zai_coder.production_api_gateway.headers import gateway_headers, security_headers, cors_headers
from zai_coder.production_api_gateway.rate_limit import rate_limit_policy_manifest
from zai_coder.production_api_gateway.upstreams import upstream_manifest, upstream_health_plan
from zai_coder.production_api_gateway.openapi import gateway_openapi_schema
from zai_coder.production_api_gateway.audit import GatewayAuditLog
from zai_coder.production_api_gateway.deploy import gateway_deploy_plan, gateway_smoke_plan
from zai_coder.production_api_gateway.ui.pages import render_gateway_overview, render_routes_page, render_upstreams_page, render_security_page


def route_gateway_status() -> dict:
    return {
        "ok": True,
        "service": "zai-production-api-gateway",
        "systems": [
            "gateway_router",
            "request_response_envelope",
            "tenant_aware_auth_guard",
            "api_key_session_guard",
            "rate_limit_policy",
            "cors_security_headers",
            "upstream_service_registry",
            "openapi_gateway_manifest",
            "gateway_error_handling",
            "gateway_audit_hooks",
        ],
    }


def route_gateway_routes() -> dict:
    return {"routes": route_manifest()}


def route_gateway_upstreams() -> dict:
    return {"upstreams": upstream_manifest(), "health_plan": upstream_health_plan()}


def route_gateway_headers() -> dict:
    return {"headers": gateway_headers(), "security": security_headers(), "cors": cors_headers()}


def route_gateway_rate_limits() -> dict:
    return {"policies": rate_limit_policy_manifest()}


def route_gateway_openapi() -> dict:
    return gateway_openapi_schema()


def route_gateway_deploy_plan() -> dict:
    return gateway_deploy_plan()


def route_gateway_smoke_plan() -> dict:
    return gateway_smoke_plan()


def route_gateway_dispatch_demo() -> dict:
    request = GatewayRequest(
        "GET",
        "/api/gateway/status",
        headers={"Origin": "http://127.0.0.1:8765"},
    )
    validation = validate_gateway_request(request)
    response = GatewayDispatcher().dispatch(request)
    GatewayAuditLog().record(request, response)
    return {"validation": validation, "response": response.to_dict()}


def route_gateway_protected_demo() -> dict:
    request = GatewayRequest(
        "GET",
        "/api/tenants/status",
        headers={
            "Authorization": "Bearer sandbox-token-123456",
            "X-Org-Id": "org_local",
            "X-Workspace-Id": "ws_default",
            "X-Actor": "admin",
        },
    )
    response = GatewayDispatcher().dispatch(request)
    GatewayAuditLog().record(request, response)
    return response.to_dict()


def route_gateway_audit() -> dict:
    return {"events": GatewayAuditLog().list_events()}


def route_gateway_page() -> dict:
    return {"content_type": "text/html", "html": render_gateway_overview()}


def route_gateway_routes_page() -> dict:
    return {"content_type": "text/html", "html": render_routes_page()}


def route_gateway_upstreams_page() -> dict:
    return {"content_type": "text/html", "html": render_upstreams_page()}


def route_gateway_security_page() -> dict:
    return {"content_type": "text/html", "html": render_security_page()}
