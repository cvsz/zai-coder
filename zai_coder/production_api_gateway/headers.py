"""CORS and security headers."""

from __future__ import annotations


def security_headers() -> dict[str, str]:
    return {
        "X-Content-Type-Options": "nosniff",
        "X-Frame-Options": "DENY",
        "Referrer-Policy": "no-referrer",
        "Permissions-Policy": "camera=(), microphone=(), geolocation=()",
        "Cache-Control": "no-store",
    }


def cors_headers(origin: str = "http://127.0.0.1:8765") -> dict[str, str]:
    allowed_local = origin.startswith("http://127.0.0.1") or origin.startswith("http://localhost")
    return {
        "Access-Control-Allow-Origin": origin if allowed_local else "http://127.0.0.1:8765",
        "Access-Control-Allow-Methods": "GET,POST,PUT,PATCH,DELETE,OPTIONS",
        "Access-Control-Allow-Headers": "Authorization,Content-Type,X-API-Key,X-Org-Id,X-Workspace-Id",
        "Access-Control-Max-Age": "300",
    }


def gateway_headers(origin: str = "http://127.0.0.1:8765") -> dict[str, str]:
    headers = security_headers()
    headers.update(cors_headers(origin))
    return headers
