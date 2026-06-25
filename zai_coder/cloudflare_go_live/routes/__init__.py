"""Cloudflare go-live route registry."""

from __future__ import annotations

from zai_coder.cloudflare_go_live.models import CloudflareGoLiveConfig
from zai_coder.cloudflare_go_live.hostname_validator import validate_hostname
from zai_coder.cloudflare_go_live.tunnel import tunnel_install_plan, render_tunnel_config
from zai_coder.cloudflare_go_live.access_policy import access_policy_checklist, access_policy_plan
from zai_coder.cloudflare_go_live.dns_planner import dns_record_plan, dns_rollback_plan
from zai_coder.cloudflare_go_live.exposure_scan import exposure_scan_plan
from zai_coder.cloudflare_go_live.public_health import public_health_verification_plan
from zai_coder.cloudflare_go_live.go_live_wizard import go_live_wizard_plan
from zai_coder.cloudflare_go_live.ui.pages import (
    render_go_live_page,
    render_access_page,
    render_dns_page,
    render_rollback_page,
    render_public_health_page,
)


def route_cloudflare_status() -> dict:
    return {
        "ok": True,
        "service": "zai-cloudflare-go-live",
        "systems": [
            "hostname_validator",
            "tunnel_installer_plan",
            "access_policy_checklist",
            "dns_record_planner",
            "tunnel_config_generator",
            "go_live_wizard",
            "preflight_exposure_scan",
            "dns_rollback_plan",
            "public_health_verification",
        ],
    }


def _cfg(payload: dict | None = None) -> CloudflareGoLiveConfig:
    payload = payload or {}
    return CloudflareGoLiveConfig(
        hostname=payload.get("hostname", "zai.example.com"),
        local_service_url=payload.get("local_service_url", "http://127.0.0.1:8765"),
        tunnel_name=payload.get("tunnel_name", "zai-coder-control-plane"),
        access_app_name=payload.get("access_app_name", "ZAI Coder Control Plane"),
        zone_name=payload.get("zone_name", "example.com"),
    )


def route_hostname_validate(payload: dict | None = None) -> dict:
    config = _cfg(payload)
    return validate_hostname(config.hostname)


def route_tunnel_plan(payload: dict | None = None) -> dict:
    return tunnel_install_plan(_cfg(payload)).to_dict()


def route_tunnel_config(payload: dict | None = None) -> dict:
    return {"content_type": "text/yaml", "yaml": render_tunnel_config(_cfg(payload))}


def route_access_checklist(payload: dict | None = None) -> dict:
    return {"items": access_policy_checklist(_cfg(payload))}


def route_access_plan(payload: dict | None = None) -> dict:
    return access_policy_plan(_cfg(payload)).to_dict()


def route_dns_plan(payload: dict | None = None) -> dict:
    return dns_record_plan(_cfg(payload)).to_dict()


def route_dns_rollback(payload: dict | None = None) -> dict:
    return dns_rollback_plan(_cfg(payload)).to_dict()


def route_exposure_scan(root: str = ".") -> dict:
    return exposure_scan_plan(root)


def route_public_health_plan(payload: dict | None = None) -> dict:
    return public_health_verification_plan(_cfg(payload)).to_dict()


def route_go_live_wizard(payload: dict | None = None) -> dict:
    return go_live_wizard_plan(_cfg(payload)).to_dict()


def route_go_live_page(payload: dict | None = None) -> dict:
    return {"content_type": "text/html", "html": render_go_live_page(_cfg(payload))}


def route_access_page(payload: dict | None = None) -> dict:
    return {"content_type": "text/html", "html": render_access_page(_cfg(payload))}


def route_dns_page(payload: dict | None = None) -> dict:
    return {"content_type": "text/html", "html": render_dns_page(_cfg(payload))}


def route_rollback_page(payload: dict | None = None) -> dict:
    return {"content_type": "text/html", "html": render_rollback_page(_cfg(payload))}


def route_public_health_page(payload: dict | None = None) -> dict:
    return {"content_type": "text/html", "html": render_public_health_page(_cfg(payload))}
