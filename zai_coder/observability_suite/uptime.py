"""Uptime verification plan."""

from __future__ import annotations


def uptime_verification_plan(base_url: str = "http://127.0.0.1:8765", public_url: str = "https://zai.example.com") -> dict:
    return {
        "dry_run": True,
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
    }
