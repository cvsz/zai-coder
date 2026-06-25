from __future__ import annotations
import json, uuid
from pathlib import Path
from .models import ApiEndpoint, SdkSnippet, Quickstart, DevAuditEvent, now_iso

ENDPOINTS = [
    ApiEndpoint("status", "GET", "/api/status", "Read local control-plane status.", "core", False, "stable"),
    ApiEndpoint("team-status", "GET", "/api/team/status", "Read team collaboration status.", "team", True, "stable"),
    ApiEndpoint("notifications-status", "GET", "/api/notifications/status", "Read notification center status.", "notifications", True, "stable"),
    ApiEndpoint("help-status", "GET", "/api/help/status", "Read help center status.", "help", True, "stable"),
    ApiEndpoint("content-status", "GET", "/api/content-studio/status", "Read template content studio status.", "content", True, "stable"),
]

SNIPPETS = [
    SdkSnippet("curl-status", "bash", "Check status with curl", "curl http://localhost:8080/api/status", "status"),
    SdkSnippet("python-team", "python", "Read team status", "import urllib.request\nprint(urllib.request.urlopen('http://localhost:8080/api/team/status').read().decode())", "team-status"),
    SdkSnippet("js-notifications", "javascript", "Read notification status", "fetch('/api/notifications/status').then(r => r.json()).then(console.log)", "notifications-status"),
]

QUICKSTARTS = [
    Quickstart("quickstart-local", "Start local developer portal", "developer", ("install package", "run local server", "open /developer", "review API docs"), "published"),
    Quickstart("quickstart-openapi", "Export OpenAPI locally", "developer", ("run make openapi-export", "inspect developer/openapi/openapi.json", "review before sharing"), "published"),
    Quickstart("quickstart-snippets", "Use examples safely", "developer", ("copy non-production snippet", "replace localhost only as needed", "never paste secrets into docs"), "published"),
]

def endpoint_registry(): return [e.to_dict() for e in ENDPOINTS]
def snippet_registry(): return [s.to_dict() for s in SNIPPETS]
def quickstart_registry(): return [q.to_dict() for q in QUICKSTARTS]

def validation_report() -> dict:
    rows = [*ENDPOINTS, *SNIPPETS, *QUICKSTARTS]
    reports = [{"id": x.id, "issues": x.validate()} for x in rows]
    return {"ok": all(not r["issues"] for r in reports), "reports": reports}

def openapi_spec() -> dict:
    paths = {}
    for e in ENDPOINTS:
        paths.setdefault(e.path, {})[e.method.lower()] = {
            "summary": e.summary,
            "tags": [e.tag],
            "x-stability": e.stability,
            "security": [{"localAuth": []}] if e.auth_required else [],
            "responses": {"200": {"description": "OK"}}
        }
    return {
        "openapi": "3.1.0",
        "info": {"title": "ZAI Coder Control Plane Local API", "version": "v41"},
        "servers": [{"url": "http://localhost:8080", "description": "local development"}],
        "components": {"securitySchemes": {"localAuth": {"type": "http", "scheme": "bearer", "description": "Use local non-production token only."}}},
        "paths": paths,
    }

def write_openapi_export(root=".", out="developer/openapi/openapi.json") -> str:
    path = Path(root) / out
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(openapi_spec(), indent=2, sort_keys=True), encoding="utf-8")
    return str(path)

def docs_export_bundle() -> dict:
    return {
        "kind": "zai-developer-portal-export",
        "version": "1.0",
        "endpoints": endpoint_registry(),
        "snippets": snippet_registry(),
        "quickstarts": quickstart_registry(),
        "validation": validation_report(),
        "openapi": openapi_spec(),
        "external_publish": False,
        "requires_review": True,
        "safety": ["no secret examples", "local server examples", "review before sharing"],
    }

def write_docs_export(root=".", out="developer/exports/developer-docs-export.json") -> str:
    path = Path(root) / out
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(docs_export_bundle(), indent=2, sort_keys=True), encoding="utf-8")
    return str(path)

def write_developer_report(root=".", out="developer/reports/developer-portal-report.md") -> str:
    path = Path(root) / out
    path.parent.mkdir(parents=True, exist_ok=True)
    endpoints = "\n".join(f"- {e.method} {e.path}: {e.summary}" for e in ENDPOINTS)
    path.write_text(f"# Developer Portal and API Docs Report\n\n## Endpoints\n\n{endpoints}\n\n## Safety\n\n- Local examples only.\n- No secret examples.\n- Review before external sharing.\n", encoding="utf-8")
    return str(path)

def developer_status():
    return {"ok": True, "systems": ["developer_portal", "api_reference", "openapi_export", "sdk_snippets", "quickstarts", "docs_export", "dashboard_routes"]}

def developer_overview():
    return {"status": developer_status(), "endpoints": endpoint_registry(), "snippets": snippet_registry(), "quickstarts": quickstart_registry(), "validation": validation_report()}

def developer_demo(root="."):
    openapi = write_openapi_export(root)
    export = write_docs_export(root)
    report = write_developer_report(root)
    return {"openapi_path": openapi, "export_path": export, "report_path": report, "bundle": docs_export_bundle()}
