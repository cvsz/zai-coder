"""Final admin UI pages."""

from __future__ import annotations

from html import escape

from .shell import render_shell


def _cards(items: list[dict]) -> str:
    return "<div class='grid'>" + "\n".join(
        f"<section class='card'><span class='badge'>{escape(str(item.get('badge', '')))}</span><h2>{escape(str(item.get('title', '')))}</h2><p>{escape(str(item.get('body', '')))}</p></section>"
        for item in items
    ) + "</div>"


def render_home_page() -> str:
    body = "<h1>Control Center</h1>" + _cards([
        {"badge": "core", "title": "Agents", "body": "Run local-first coding, creative, and deployment workflows."},
        {"badge": "saas", "title": "SaaS", "body": "Manage organizations, users, workspaces, billing, quota, and audit."},
        {"badge": "deploy", "title": "Deploy", "body": "Plan Docker, systemd, Cloudflare, and release artifacts safely."},
        {"badge": "integrations", "title": "Integrations", "body": "Generate dry-run plans for GitHub, Cloudflare, Docker, Hugging Face, social, storage, and notifications."},
    ])
    return render_shell("ZAI App Studio", body, "Dashboard")


def render_plugins_page(plugins: list[dict]) -> str:
    body = "<h1>Plugin Marketplace</h1>" + _cards([
        {"badge": p.get("category", "plugin"), "title": p.get("name", ""), "body": p.get("description", "")}
        for p in plugins
    ])
    return render_shell("Plugins", body, "Plugins")


def render_workflows_page(workflows: list[dict]) -> str:
    body = "<h1>AI Workflow Builder</h1>" + _cards([
        {"badge": w.get("status", "draft"), "title": w.get("name", ""), "body": " → ".join(w.get("steps", []))}
        for w in workflows
    ])
    return render_shell("Workflows", body, "Workflows")


def render_models_page(models: list[dict]) -> str:
    body = "<h1>Model Router</h1>" + _cards([
        {"badge": m.get("provider", "local"), "title": m.get("name", ""), "body": m.get("purpose", "")}
        for m in models
    ])
    return render_shell("Models", body, "Models")


def render_deployments_page(deployments: list[dict]) -> str:
    body = "<h1>Deployment Control Center</h1>" + _cards([
        {"badge": d.get("target", "local"), "title": d.get("name", ""), "body": d.get("status", "planned")}
        for d in deployments
    ])
    return render_shell("Deployments", body, "Deployments")
