from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
from pathlib import Path

from .config import ensure_config, load_config
from .core.messages import Message
from .core.models import ModelRouter, provider_from_config
from .core.orchestrator import MultiAgentOrchestrator
from .core.audit import AuditLog
from .core.memory import MemoryStore
from .core.patcher import PatchRuntime
from .core.project import scan_project
from .core.registry import JsonRegistry
from .core.safety import SafetyPolicy
from .core.self_core import (
    next_requirements_markdown,
    run_self_doctor,
    runbook,
    self_features_markdown,
    write_text_safely,
)
from .core.tools import ToolRuntime
from .agents.registry import build_agent
from .media import generate_svg_image, generate_voice_wav, generate_music_wav, generate_animation_svg, generate_video_storyboard

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"


def print_box(title: str, body: str) -> None:
    print(f"\n== {title} ==")
    print(body.rstrip())


def build_router(cfg):
    provider = provider_from_config(cfg.provider, cfg.base_url)
    return ModelRouter(provider)


def cmd_doctor(args) -> int:
    path = ensure_config(args.config)
    cfg = load_config(str(path))
    print_box("Config", json.dumps(cfg.to_dict(), indent=2))
    print_box("Python", sys.version.split()[0])
    print_box("Workspace", str(Path(cfg.workspace).expanduser().resolve()))
    ollama = shutil.which("ollama")
    print_box("Ollama", ollama or "not found")
    if ollama:
        runtime = ToolRuntime(workspace=".", safety=SafetyPolicy(), timeout=20)
        result = runtime.run("ollama list")
        print(result.stdout or result.stderr)
    return 0


def cmd_agents(args) -> int:
    reg = JsonRegistry(ASSETS / "agents")
    for item in reg.list():
        print(f"- {item.name}: {item.description} [{', '.join(item.tags)}]")
    return 0


def cmd_skills(args) -> int:
    reg = JsonRegistry(ASSETS / "skills")
    for item in reg.list():
        print(f"- {item.name}: {item.description} [{', '.join(item.tags)}]")
    return 0


def cmd_ask(args) -> int:
    cfg = load_config(args.config)
    router = build_router(cfg)
    agent = build_agent(args.agent)
    prompt = agent.build_prompt(type("Ctx", (), {"task": args.prompt, "memory": {}})())
    messages = [
        Message("system", "You are ZAI Coder. Follow safe repo rules. Do not suggest git add ."),
        Message("user", prompt),
    ]
    res = router.chat_with_fallbacks(messages, cfg.model, cfg.fallback_models, cfg.temperature, cfg.max_tokens)
    print(res.content)
    print(f"\n[model={res.model} provider={res.provider}]")
    return 0


def cmd_chat(args) -> int:
    cfg = load_config(args.config)
    router = build_router(cfg)
    agent = build_agent(args.agent)
    messages = [Message("system", "You are ZAI Coder. Be safe, concise, and practical. Never suggest git add .")]
    print("ZAI Coder chat. Type /bye to exit.")
    while True:
        try:
            user = input(">>> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return 0
        if user in {"/bye", "/exit", "quit"}:
            return 0
        prompt = agent.build_prompt(type("Ctx", (), {"task": user, "memory": {}})())
        messages.append(Message("user", prompt))
        res = router.chat_with_fallbacks(messages, cfg.model, cfg.fallback_models, cfg.temperature, cfg.max_tokens)
        messages.append(Message("assistant", res.content))
        print(res.content)
        print(f"[model={res.model} provider={res.provider}]")


def cmd_plan(args) -> int:
    cfg = load_config(args.config)
    router = build_router(cfg)
    names = [n.strip() for n in args.agents.split(",") if n.strip()]
    agents = [build_agent(n) for n in names]
    orchestrator = MultiAgentOrchestrator(router, cfg.model, cfg.fallback_models, cfg.temperature, cfg.max_tokens)
    result = orchestrator.run(args.task, agents)
    print(result.content)
    print(f"\n[steps={', '.join(result.steps)} model={result.model} provider={result.provider}]")
    return 0


def cmd_run(args) -> int:
    cfg = load_config(args.config)
    runtime = ToolRuntime(workspace=cfg.workspace, safety=SafetyPolicy(cfg.allow_apps_zlms), timeout=cfg.tool_timeout_seconds)
    res = runtime.run(args.command)
    if res.blocked_reason:
        print(f"BLOCKED: {res.blocked_reason}")
        return res.exit_code
    if res.stdout:
        print(res.stdout, end="")
    if res.stderr:
        print(res.stderr, end="", file=sys.stderr)
    return res.exit_code


def cmd_scan(args) -> int:
    cfg = load_config(args.config)
    scan = scan_project(cfg.workspace)
    print(scan.to_markdown())
    return 0


def cmd_audit(args) -> int:
    cfg = load_config(args.config)
    events = AuditLog(Path(cfg.workspace) / "data" / "zai-audit.jsonl").tail(args.limit)
    print(json.dumps(events, indent=2))
    return 0


def cmd_memory(args) -> int:
    cfg = load_config(args.config)
    store = MemoryStore(Path(cfg.workspace) / "data" / "zai-memory.db")
    if args.memory_cmd == "list":
        items = store.list(namespace=args.namespace, limit=args.limit)
        print(json.dumps([item.__dict__ for item in items], indent=2))
        return 0
    if args.memory_cmd == "get":
        value = store.get(args.key, namespace=args.namespace)
        print(value or "")
        return 0 if value is not None else 1
    raise SystemExit(f"Unknown memory command: {args.memory_cmd}")


def cmd_patch(args) -> int:
    cfg = load_config(args.config)
    runtime = PatchRuntime(cfg.workspace, Path(".zai-coder") / "checkpoints", SafetyPolicy(cfg.allow_apps_zlms))
    result = runtime.apply_file(args.patch_file, check_only=not args.apply)
    if result.stdout:
        print(result.stdout, end="")
    if result.stderr:
        print(result.stderr, end="", file=sys.stderr)
    if result.blocked_reason:
        print(f"BLOCKED: {result.blocked_reason}", file=sys.stderr)
    if result.checkpoint:
        print(f"checkpoint: {result.checkpoint}")
    return 0 if result.ok else 1


def cmd_serve(args) -> int:
    if args.host not in {"127.0.0.1", "localhost"}:
        print("Remote bind is disabled by default; use 127.0.0.1 or localhost.", file=sys.stderr)
        return 2
    print(f"Local server plan: host={args.host} port={args.port}. Use deployment scripts for approved runtime start.")
    return 0


def cmd_self(args) -> int:
    if args.self_cmd == "list":
        print(self_features_markdown())
        return 0
    if args.self_cmd == "doctor":
        print(json.dumps(run_self_doctor(Path.cwd()), indent=2))
        return 0
    if args.self_cmd == "plan":
        print(next_requirements_markdown())
        return 0
    if args.self_cmd == "requirement-next":
        content = next_requirements_markdown()
        if args.out:
            out = write_text_safely(args.out, content, Path.cwd())
            print(out)
        else:
            print(content)
        return 0
    if args.self_cmd == "runbook":
        print(runbook(args.feature), end="")
        return 0
    raise SystemExit(f"Unknown self command: {args.self_cmd}")


def cmd_media(args) -> int:
    if args.kind == "image":
        out = generate_svg_image(args.prompt, args.out)
    elif args.kind == "voice":
        out = generate_voice_wav(args.text or args.prompt, args.out)
    elif args.kind == "music":
        out = generate_music_wav(args.prompt, args.out)
    elif args.kind == "animation":
        out = generate_animation_svg(args.prompt, args.out)
    elif args.kind == "video":
        out = generate_video_storyboard(args.prompt, args.out)
    else:
        raise SystemExit(f"Unknown media kind: {args.kind}")
    print(out)
    return 0

def cmd_tui(args) -> int:
    from .tui.app import describe_templates, run_tui
    from .tui.config import load_tui_config

    if args.list_templates:
        print(describe_templates())
        return 0
    if args.print_config:
        print(json.dumps(load_tui_config(), indent=2))
        return 0
    return run_tui(args.template, args.dry_run, args.no_textual)

def build_parser() -> argparse.ArgumentParser:

    p = argparse.ArgumentParser(prog="zai-coder", description="Standalone local-first AI coding and media-agent CLI")
    p.add_argument("--config", default=None, help="Path to config JSON")
    sub = p.add_subparsers(dest="cmd", required=True)

    d = sub.add_parser("doctor")
    d.set_defaults(func=cmd_doctor)

    a = sub.add_parser("agents")
    a.set_defaults(func=cmd_agents)

    s = sub.add_parser("skills")
    s.set_defaults(func=cmd_skills)

    ask = sub.add_parser("ask")
    ask.add_argument("prompt")
    ask.add_argument("--agent", default="coder")
    ask.set_defaults(func=cmd_ask)

    chat = sub.add_parser("chat")
    chat.add_argument("--agent", default="coder")
    chat.set_defaults(func=cmd_chat)

    plan = sub.add_parser("plan")
    plan.add_argument("--task", required=True)
    plan.add_argument("--agents", default="planner,coder,reviewer")
    plan.set_defaults(func=cmd_plan)

    run = sub.add_parser("run")
    run.add_argument("command")
    run.set_defaults(func=cmd_run)

    scan = sub.add_parser("scan")
    scan.set_defaults(func=cmd_scan)

    audit = sub.add_parser("audit")
    audit.add_argument("--limit", type=int, default=50)
    audit.set_defaults(func=cmd_audit)

    serve = sub.add_parser("serve")
    serve.add_argument("--host", default="127.0.0.1")
    serve.add_argument("--port", type=int, default=8765)
    serve.set_defaults(func=cmd_serve)

    memory = sub.add_parser("memory")
    memory_sub = memory.add_subparsers(dest="memory_cmd", required=True)
    memory_list = memory_sub.add_parser("list")
    memory_list.add_argument("--namespace", default="default")
    memory_list.add_argument("--limit", type=int, default=100)
    memory_list.set_defaults(func=cmd_memory)
    memory_get = memory_sub.add_parser("get")
    memory_get.add_argument("key")
    memory_get.add_argument("--namespace", default="default")
    memory_get.set_defaults(func=cmd_memory)

    patch = sub.add_parser("patch")
    patch.add_argument("patch_file")
    patch.add_argument("--apply", action="store_true")
    patch.set_defaults(func=cmd_patch)

    self_cmd = sub.add_parser("self")
    self_sub = self_cmd.add_subparsers(dest="self_cmd", required=True)
    self_list = self_sub.add_parser("list")
    self_list.set_defaults(func=cmd_self)
    self_doctor = self_sub.add_parser("doctor")
    self_doctor.set_defaults(func=cmd_self)
    self_plan = self_sub.add_parser("plan")
    self_plan.set_defaults(func=cmd_self)
    self_req = self_sub.add_parser("requirement-next")
    self_req.add_argument("--out", default="")
    self_req.set_defaults(func=cmd_self)
    self_runbook = self_sub.add_parser("runbook")
    self_runbook.add_argument("feature")
    self_runbook.set_defaults(func=cmd_self)

    media = sub.add_parser("media")
    media.add_argument("kind", choices=["image", "voice", "music", "animation", "video"])
    media.add_argument("--prompt", default="ZAI Coder")
    media.add_argument("--text", default="")
    media.add_argument("--out", default="out/artifact")
    media.set_defaults(func=cmd_media)

    tui = sub.add_parser("tui")
    tui.add_argument("--template", help="Template name")
    tui.add_argument("--dry-run", action="store_true")
    tui.add_argument("--no-textual", action="store_true")
    tui.add_argument("--print-config", action="store_true")
    tui.add_argument("--list-templates", action="store_true")
    tui.set_defaults(func=cmd_tui)

    return p


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
