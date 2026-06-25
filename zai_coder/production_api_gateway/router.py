"""Production gateway route registry and dispatcher."""

from __future__ import annotations

from .models import GatewayRequest, GatewayRoute
from .auth import auth_decision
from .tenant_context import require_tenant_context
from .rate_limit import InMemoryRateLimiter
from .envelope import success_response, error_response
from .headers import gateway_headers


DEFAULT_ROUTES = [
    GatewayRoute("status", "GET", "/api/gateway/status", "core", False, False, "standard", "Gateway status"),
    GatewayRoute("tenants", "GET", "/api/tenants/status", "tenants", True, True, "standard", "Tenant status"),
    GatewayRoute("billing", "GET", "/api/billing/status", "billing", True, True, "standard", "Billing status"),
    GatewayRoute("payments", "GET", "/api/payments/status", "billing", True, True, "strict", "Payment status"),
    GatewayRoute("ops", "GET", "/api/ops/status", "ops", True, True, "admin", "Operations status"),
]


def route_manifest() -> list[dict]:
    return [route.to_dict() for route in DEFAULT_ROUTES]


def find_route(method: str, path: str) -> GatewayRoute | None:
    method = method.upper()
    for route in DEFAULT_ROUTES:
        if route.method.upper() == method and route.path == path:
            return route
    return None


class GatewayDispatcher:
    def __init__(self, limiter: InMemoryRateLimiter | None = None):
        self.limiter = limiter or InMemoryRateLimiter()

    def dispatch(self, request: GatewayRequest):
        route = find_route(request.method, request.path)
        headers = gateway_headers(request.headers.get("Origin", "http://127.0.0.1:8765"))
        if route is None:
            response = error_response("not_found", "route not found", 404)
            return response.__class__(response.status, response.body, {**headers, **response.headers})

        issues = route.validate()
        if issues:
            response = error_response("route_invalid", "; ".join(issues), 500)
            return response.__class__(response.status, response.body, {**headers, **response.headers})

        auth = auth_decision(request, route.auth_required)
        if not auth["allowed"]:
            response = error_response("unauthorized", auth["reason"], 401)
            return response.__class__(response.status, response.body, {**headers, **response.headers})

        tenant = require_tenant_context(request) if route.tenant_required else {"allowed": True, "context": {"org_id": "public", "workspace_id": "public", "actor": auth.get("actor", "public")}}
        if not tenant["allowed"]:
            response = error_response("tenant_required", tenant["reason"], 400)
            return response.__class__(response.status, response.body, {**headers, **response.headers})

        identity = f"{tenant['context']['org_id']}:{tenant['context']['workspace_id']}:{auth.get('actor','unknown')}"
        rate = self.limiter.check(identity, route.rate_limit_key)
        if not rate["allowed"]:
            response = error_response("rate_limited", "rate limit exceeded", 429)
            return response.__class__(response.status, response.body, {**headers, **response.headers})

        response = success_response({"route": route.to_dict(), "tenant": tenant["context"], "rate_limit": rate})
        return response.__class__(response.status, response.body, {**headers, **response.headers})
