"""Healthcheck command plan."""

from __future__ import annotations


def healthcheck_plan(base_url: str = "http://127.0.0.1:8765") -> dict:
    return {
        "dry_run": True,
        "base_url": base_url,
        "commands": [
            f"curl -fsS {base_url}/healthz",
            f"curl -fsS {base_url}/readyz",
            f"curl -fsS {base_url}/openapi.json",
        ],
    }
