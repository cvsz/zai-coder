"""OpenAPI gateway manifest."""

from __future__ import annotations

from .router import route_manifest


def gateway_openapi_schema() -> dict:
    paths: dict = {}
    for route in route_manifest():
        method = route["method"].lower()
        paths.setdefault(route["path"], {})[method] = {
            "summary": route["description"] or route["id"],
            "x-upstream": route["upstream"],
            "x-auth-required": route["auth_required"],
            "x-tenant-required": route["tenant_required"],
            "responses": {
                "200": {"description": "Gateway envelope success"},
                "400": {"description": "Bad request"},
                "401": {"description": "Unauthorized"},
                "429": {"description": "Rate limited"},
            },
        }
    return {
        "openapi": "3.1.0",
        "info": {"title": "ZAI Coder Production API Gateway", "version": "v24"},
        "paths": paths,
        "components": {"securitySchemes": {"BearerAuth": {"type": "http", "scheme": "bearer"}, "ApiKeyAuth": {"type": "apiKey", "in": "header", "name": "X-API-Key"}}},
    }
