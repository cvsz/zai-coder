"""Upstream service registry."""

from __future__ import annotations

from .models import UpstreamService


DEFAULT_UPSTREAMS = {
    "core": UpstreamService("core", "Core API", "http://127.0.0.1:8765"),
    "ops": UpstreamService("ops", "Operations", "http://127.0.0.1:8765"),
    "billing": UpstreamService("billing", "Billing", "http://127.0.0.1:8765"),
    "tenants": UpstreamService("tenants", "Tenants", "http://127.0.0.1:8765"),
}


def upstream_manifest() -> list[dict]:
    return [service.to_dict() for service in DEFAULT_UPSTREAMS.values()]


def get_upstream(upstream_id: str) -> UpstreamService:
    if upstream_id not in DEFAULT_UPSTREAMS:
        raise ValueError(f"unknown upstream: {upstream_id}")
    service = DEFAULT_UPSTREAMS[upstream_id]
    issues = service.validate()
    if issues:
        raise ValueError("; ".join(issues))
    return service


def upstream_health_plan() -> dict:
    return {
        "dry_run": True,
        "checks": [
            {"id": service.id, "name": service.name, "url": service.base_url + service.health_path, "timeout_seconds": service.timeout_seconds}
            for service in DEFAULT_UPSTREAMS.values()
        ],
    }
