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
from .core.registry import JsonRegistry
from .core.safety import SafetyPolicy
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

    media = sub.add_parser("media")
    media.add_argument("kind", choices=["image", "voice", "music", "animation", "video"])
    media.add_argument("--prompt", default="ZAI Coder")
    media.add_argument("--text", default="")
    media.add_argument("--out", default="out/artifact")
    media.set_defaults(func=cmd_media)

    return p


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
