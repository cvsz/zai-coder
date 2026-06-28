"""Uptime verification plan."""

from __future__ import annotations


def uptime_verification_plan(base_url: str = "http://127.0.0.1:8765", public_url: str = "https://zai.example.com", execute: bool = False) -> dict:
    results = []
    if execute:
        import urllib.request
        def check_url(url):
            try:
                urllib.request.urlopen(url, timeout=2)
                return "UP"
            except Exception as e:
                return f"DOWN: {str(e)}"
        results = [
            {"target": f"{base_url}/healthz", "status": check_url(f"{base_url}/healthz")},
            {"target": f"{public_url}/healthz", "status": check_url(f"{public_url}/healthz")},
        ]
        
    return {
        "dry_run": not execute,
        "local_checks": [
            f"curl -fsS {base_url}/healthz",
            f"curl -fsS {base_url}/readyz",
            f"curl -fsS {base_url}/api/execution/status",
        ],
        "public_checks": [
            f"curl -I {public_url}/healthz",
            f"curl -I {public_url}/api/status",
        ],
        "expected": [
            "local health returns 200",
            "local readiness returns 200",
            "public protected API returns Access challenge or 401/403",
        ],
        "live_results": results
    }
