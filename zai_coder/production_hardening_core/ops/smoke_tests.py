"""Production smoke test plan."""

from __future__ import annotations


def production_smoke_test_plan(base_url: str = "http://127.0.0.1:8765") -> dict:
    return {
        "base_url": base_url,
        "checks": [
            {"name": "health", "method": "GET", "url": f"{base_url}/healthz", "expect": 200},
            {"name": "ready", "method": "GET", "url": f"{base_url}/readyz", "expect": 200},
            {"name": "openapi", "method": "GET", "url": f"{base_url}/openapi.json", "expect": 200},
            {"name": "status-auth-required", "method": "GET", "url": f"{base_url}/api/status", "expect": 401},
        ],
        "dry_run": True,
    }
