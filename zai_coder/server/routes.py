import json
from pathlib import Path
from zai_coder.core.tools import ToolRuntime
from zai_coder.core.safety import SafetyPolicy
from zai_coder.core.registry import JsonRegistry
from zai_coder.core.audit import AuditLog
from zai_coder.core.self_core import self_features_markdown, run_self_doctor
from zai_coder.cli import _ask, build_agent, MultiAgentOrchestrator, build_router
from zai_coder.config import load_config
from zai_coder.server.http import JsonHTTPRequestHandler

def handle_get(handler: JsonHTTPRequestHandler, path: str):
    if path == "/health":
        handler.send_json_response(200, {"status": "ok"})
    elif path == "/version":
        import zai_coder
        handler.send_json_response(200, {"version": zai_coder.__version__})
    elif path == "/agents":
        reg = JsonRegistry(Path("assets/agents").resolve())
        agents = [{"name": item.name, "description": item.description} for item in reg.list()]
        handler.send_json_response(200, {"agents": agents})
    elif path == "/skills":
        reg = JsonRegistry(Path("assets/skills").resolve())
        skills = [{"name": item.name, "description": item.description} for item in reg.list()]
        handler.send_json_response(200, {"skills": skills})
    elif path == "/self/features":
        handler.send_json_response(200, {"features": self_features_markdown()})
    elif path == "/self/status":
        handler.send_json_response(200, {"status": run_self_doctor(Path.cwd())})
    else:
        handler.send_json_response(404, {"error": "Not Found"})

def handle_post(handler: JsonHTTPRequestHandler, path: str, body: dict, config_path: str = None):
    cfg = load_config(config_path)
    audit = AuditLog(Path(cfg.workspace) / "data" / "zai-audit.jsonl")
    
    if path == "/ask":
        audit.write("api_ask", True, "API Ask", prompt=body.get("prompt"))
        res = _ask(cfg, body.get("prompt", ""), body.get("agent", "coder"))
        handler.send_json_response(200, {"content": res.content, "model": res.model})
    elif path == "/plan":
        audit.write("api_plan", True, "API Plan", task=body.get("task"))
        router = build_router(cfg)
        names = body.get("agents", ["planner", "coder", "reviewer"])
        agents = [build_agent(n) for n in names]
        orchestrator = MultiAgentOrchestrator(router, cfg.model, cfg.fallback_models, cfg.temperature, cfg.max_tokens)
        res = orchestrator.run(body.get("task", ""), agents)
        handler.send_json_response(200, {"content": res.content, "steps": res.steps})
    elif path == "/run":
        audit.write("api_run", True, "API Run", command=body.get("command"))
        runtime = ToolRuntime(workspace=cfg.workspace, safety=SafetyPolicy(cfg.allow_apps_zlms), timeout=cfg.tool_timeout_seconds)
        res = runtime.run(body.get("command", ""))
        handler.send_json_response(200, {
            "exit_code": res.exit_code,
            "stdout": res.stdout,
            "stderr": res.stderr,
            "blocked_reason": res.blocked_reason
        })
    else:
        handler.send_json_response(404, {"error": "Not Found"})
