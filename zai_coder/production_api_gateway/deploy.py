"""API gateway deployment plan."""

from __future__ import annotations


def gateway_deploy_plan() -> dict:
    return {
        "dry_run": True,
        "steps": [
            "run tests",
            "verify route manifest",
            "verify upstream localhost targets",
            "enable gateway audit log",
            "verify security headers",
            "verify tenant context guard",
            "run rate-limit smoke tests",
            "expose through Cloudflare Access only",
        ],
        "commands": [
            "python3 -m pytest -q",
            "make gateway-status",
            "make gateway-routes",
            "make gateway-upstreams",
            "make gateway-smoke-test",
            "make cloudflare-access-checklist",
        ],
    }


def gateway_smoke_plan() -> dict:
    return {
        "dry_run": True,
        "checks": [
            "GET /api/gateway/status returns envelope",
            "Protected route without auth returns 401",
            "Protected route without tenant context returns 400",
            "Security headers are present",
            "Rate limiter returns remaining counter",
        ],
    }

def production_gateway_profile() -> dict:
    return {
        "tls_termination": "expected_from_cloudflare",
        "upstream_health_failover": True,
        "request_size_limit_mb": 10,
        "rate_limits": {
            "global": "100/min",
            "auth": "10/min"
        },
        "structured_audit_logging": True,
        "strict_security_headers": True,
    }
