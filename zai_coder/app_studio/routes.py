"""Framework-neutral App Studio route registry."""

from __future__ import annotations

from .dashboard import render_app_studio_dashboard


def route_status() -> dict:
    return {
        "ok": True,
        "service": "zai-app-studio",
        "systems": [
            "members",
            "billing",
            "workspaces",
            "creative",
            "agents",
            "audit",
            "api_auth",
            "migrations",
            "worker",
            "streaming",
        ],
    }


def route_dashboard(payload: dict) -> dict:
    html = render_app_studio_dashboard(
        payload.get("projects", []),
        payload.get("members", []),
        payload.get("plans", []),
        payload.get("runs", []),
        payload.get("audit_events", []),
    )
    return {"content_type": "text/html", "html": html}
