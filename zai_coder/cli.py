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


def build_audit(cfg) -> AuditLog:
    return AuditLog(Path(cfg.workspace) / "data" / "zai-audit.jsonl")


def build_memory(cfg) -> MemoryStore:
    return MemoryStore(Path(cfg.workspace) / "data" / "zai-memory.jsonl")


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


def _ask(cfg, prompt_text: str, agent_name: str):
    router = build_router(cfg)
    agent = build_agent(agent_name)
    prompt = agent.build_prompt(type("Ctx", (), {"task": prompt_text, "memory": {}})())
    messages = [
        Message("system", "You are ZAI Coder. Follow safe repo rules. Do not suggest git add ."),
        Message("user", prompt),
    ]
    return router.chat_with_fallbacks(messages, cfg.model, cfg.fallback_models, cfg.temperature, cfg.max_tokens)


def cmd_ask(args) -> int:
    cfg = load_config(args.config)
    prompt_text = args.prompt
    if getattr(args, "with_rag", False):
        from zai_coder.core.rag import LocalRAG
        rag = LocalRAG(cfg.workspace)
        context = rag.query(prompt_text)
        prompt_text = f"Context:\n{context}\n\nTask:\n{prompt_text}"
        
    res = _ask(cfg, prompt_text, args.agent)
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
    if getattr(args, "format", "json") == "json":
        print(json.dumps(events, indent=2))
    else:
        # Table format
        print("| Timestamp | Action | OK |")
        print("|---|---|---|")
        for e in events:
            print(f"| {e.get('timestamp', '')} | {e.get('action', '')} | {e.get('ok', False)} |")
    return 0


def cmd_metrics(args) -> int:
    from .core.monitor import get_metrics
    print(json.dumps(get_metrics(Path.cwd()), indent=2))
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
    cfg = load_config(args.config)
    if args.host not in {"127.0.0.1", "localhost"} and not getattr(cfg, "remote_bind_enabled", False):
        print("Remote bind is disabled by default; use 127.0.0.1 or localhost.", file=sys.stderr)
        return 2
    
    from zai_coder.server.app import run_server
    print(f"Starting local server on {args.host}:{args.port}")
    try:
        run_server(args.host, args.port, args.config)
    except KeyboardInterrupt:
        pass
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
    if args.self_cmd == "monitor":
        from .core.monitor import get_metrics, format_metrics_markdown
        print(format_metrics_markdown(get_metrics(Path.cwd())))
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

def cmd_index(args) -> int:
    from .core.indexer import ProjectIndexer
    from .config import load_config
    cfg = load_config(args.config)
    indexer = ProjectIndexer(Path(cfg.workspace) / "data" / "index.db")
    if args.index_cmd == "build":
        indexer.build(cfg.workspace)
        print("Index built.")
    elif args.index_cmd == "search":
        results = indexer.search(args.query)
        for r in results:
            print(f"{r['path']} (score: {r['score']})")
    return 0

def cmd_rag(args) -> int:
    from .core.rag import LocalRAG
    from .config import load_config
    cfg = load_config(args.config)
    rag = LocalRAG(cfg.workspace)
    if args.rag_cmd == "build":
        rag.build()
        print("RAG index built.")
    elif args.rag_cmd == "query":
        print(rag.query(args.query))
    return 0

def cmd_task(args) -> int:
    from .core.tasks import TaskQueue
    from .core.approvals import ApprovalGate
    from .config import load_config
    from .cli import _ask
    import json
    cfg = load_config(args.config)
    queue = TaskQueue(Path(cfg.workspace) / "data" / "tasks.db")
    
    if args.task_cmd == "create":
        task_id = queue.create(args.title, args.agent, args.prompt)
        print(f"Task {task_id} created.")
    elif args.task_cmd == "list":
        for t in queue.list_tasks():
            print(f"[{t['id']}] {t['state'].upper()}: {t['title']} (agent: {t['agent']})")
    elif args.task_cmd == "show":
        t = queue.get(args.task_id)
        if not t:
            print("Task not found.")
            return 1
        print(json.dumps(t, indent=2))
    elif args.task_cmd == "cancel":
        if queue.transition(args.task_id, ["queued", "waiting_approval", "running"], "cancelled"):
            print("Task cancelled.")
        else:
            print("Could not cancel task.")
            return 1
    elif args.task_cmd == "logs":
        t = queue.get(args.task_id)
        if not t:
            print("Task not found.")
            return 1
        print(f"Output:\n{t['output']}\nError:\n{t['error']}")
    elif args.task_cmd == "run":
        gate = ApprovalGate(getattr(args, "apply", False))
        t = queue.get(args.task_id)
        if not t or t["state"] not in ("queued", "waiting_approval"):
            print("Task not ready to run.")
            return 1
            
        if not gate.check():
            queue.update_state(args.task_id, "waiting_approval")
            print("Dry run: task requires --apply to run. State changed to waiting_approval.")
            return 0
            
        queue.update_state(args.task_id, "running")
        try:
            res = _ask(cfg, t["prompt"], t["agent"])
            queue.update_state(args.task_id, "completed", output=res.content)
            print(f"Task completed:\n{res.content}")
        except Exception as e:
            queue.update_state(args.task_id, "failed", error=str(e))
            print(f"Task failed: {e}")
            return 1
    return 0

def cmd_policy(args) -> int:
    from .core.policy_loader import PolicyLoader
    import json
    
    loader = PolicyLoader()
    
    if args.policy_cmd == "list":
        policies = loader.list_policies()
        print("Available policies:")
        for p in sorted(policies):
            print(f"  - {p}")
        return 0
        
    elif args.policy_cmd == "show":
        try:
            policy = loader.load(args.profile)
            import dataclasses
            print(json.dumps(dataclasses.asdict(policy), indent=2))
        except ValueError as e:
            print(f"Error: {e}")
            return 1
        return 0
        
    elif args.policy_cmd == "check":
        try:
            policy = loader.load(args.profile)
            ok, reason = policy.check_command(args.command)
            if not ok:
                print(f"Command check: BLOCKED - {reason}")
                return 1
                
            from .core.safety import SafetyPolicy
            sp = SafetyPolicy()
            sr = sp.check_command(args.command)
            if not sr.allowed:
                print(f"Command check: BLOCKED - {sr.reason}")
                return 1
                
            print("Command check: OK")
            return 0
        except ValueError as e:
            print(f"Error: {e}")
            return 1
            
    elif args.policy_cmd == "check-path":
        try:
            policy = loader.load(args.profile)
            ok, reason = policy.check_path(args.path)
            if not ok:
                print(f"Path check: BLOCKED - {reason}")
                return 1
                
            from .core.safety import SafetyPolicy
            sp = SafetyPolicy()
            sr = sp.check_path(args.path)
            if not sr.allowed:
                print(f"Path check: BLOCKED - {sr.reason}")
                return 1
                
            print("Path check: OK")
            return 0
        except ValueError as e:
            print(f"Error: {e}")
            return 1
            
    print("Invalid policy command")
    return 1

def cmd_migrate(args) -> int:
    from .core.migrations import MigrationManager
    import json
    manager = MigrationManager()
    
    if args.migrate_cmd == "status":
        print(json.dumps(manager.status(), indent=2))
        return 0
    elif args.migrate_cmd == "apply":
        apply = getattr(args, "apply", False)
        results = manager.apply(dry_run=not apply)
        for r in results:
            print(r)
        if not results:
            print("No pending migrations.")
        return 0
    return 0

def cmd_update(args) -> int:
    from .core.update import check_update, plan_update
    from .config import load_config
    import json
    cfg = load_config(args.config)
    
    if args.update_cmd == "check":
        print(json.dumps(check_update(cfg.workspace, args.local_manifest), indent=2))
        return 0
    elif args.update_cmd == "plan":
        print(json.dumps(plan_update(cfg.workspace, args.local_manifest), indent=2))
        return 0
    return 0

def cmd_tui(args) -> int:
    from .tui.app import run_tui

    try:
        return run_tui(
            args.template,
            args.dry_run,
            args.no_textual,
            print_config=args.print_config,
            list_templates=args.list_templates,
        )
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2

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
    ask.add_argument("--with-rag", action="store_true")
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
    audit.add_argument("--limit", type=int, default=100)
    audit.add_argument("--format", choices=["json", "table"], default="json")
    audit.set_defaults(func=cmd_audit)

    metrics = sub.add_parser("metrics")
    metrics_sub = metrics.add_subparsers(dest="metrics_cmd", required=True)
    metrics_snap = metrics_sub.add_parser("snapshot")
    metrics_snap.set_defaults(func=cmd_metrics)

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
    self_monitor = self_sub.add_parser("monitor")
    self_monitor.set_defaults(func=cmd_self)

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

    index = sub.add_parser("index")
    index_sub = index.add_subparsers(dest="index_cmd", required=True)
    index_build = index_sub.add_parser("build")
    index_build.set_defaults(func=cmd_index)
    index_search = index_sub.add_parser("search")
    index_search.add_argument("query")
    index_search.set_defaults(func=cmd_index)

    rag = sub.add_parser("rag")
    rag_sub = rag.add_subparsers(dest="rag_cmd", required=True)
    rag_build = rag_sub.add_parser("build")
    rag_build.set_defaults(func=cmd_rag)
    rag_query = rag_sub.add_parser("query")
    rag_query.add_argument("query")
    rag_query.set_defaults(func=cmd_rag)

    task = sub.add_parser("task")
    task_sub = task.add_subparsers(dest="task_cmd", required=True)
    task_create = task_sub.add_parser("create")
    task_create.add_argument("--title", required=True)
    task_create.add_argument("--agent", required=True)
    task_create.add_argument("--prompt", required=True)
    task_create.set_defaults(func=cmd_task)
    task_list = task_sub.add_parser("list")
    task_list.set_defaults(func=cmd_task)
    task_show = task_sub.add_parser("show")
    task_show.add_argument("task_id", type=int)
    task_show.set_defaults(func=cmd_task)
    task_run = task_sub.add_parser("run")
    task_run.add_argument("task_id", type=int)
    task_run.add_argument("--dry-run", action="store_false", dest="apply", default=False)
    task_run.add_argument("--apply", action="store_true")
    task_run.set_defaults(func=cmd_task)
    task_logs = task_sub.add_parser("logs")
    task_logs.add_argument("task_id", type=int)
    task_logs.set_defaults(func=cmd_task)
    task_cancel = task_sub.add_parser("cancel")
    task_cancel.add_argument("task_id", type=int)
    task_cancel.set_defaults(func=cmd_task)

    policy = sub.add_parser("policy")
    policy_sub = policy.add_subparsers(dest="policy_cmd", required=True)
    policy_list = policy_sub.add_parser("list")
    policy_list.set_defaults(func=cmd_policy)
    policy_show = policy_sub.add_parser("show")
    policy_show.add_argument("profile")
    policy_show.set_defaults(func=cmd_policy)
    policy_check = policy_sub.add_parser("check")
    policy_check.add_argument("--command", required=True)
    policy_check.add_argument("--profile", required=True)
    policy_check.set_defaults(func=cmd_policy)
    policy_check_path = policy_sub.add_parser("check-path")
    policy_check_path.add_argument("path")
    policy_check_path.add_argument("--profile", required=True)
    policy_check_path.set_defaults(func=cmd_policy)

    migrate = sub.add_parser("migrate")
    migrate_sub = migrate.add_subparsers(dest="migrate_cmd", required=True)
    migrate_status = migrate_sub.add_parser("status")
    migrate_status.set_defaults(func=cmd_migrate)
    migrate_apply = migrate_sub.add_parser("apply")
    migrate_apply.add_argument("--dry-run", action="store_false", dest="apply", default=False)
    migrate_apply.add_argument("--apply", action="store_true")
    migrate_apply.set_defaults(func=cmd_migrate)

    update = sub.add_parser("update")
    update_sub = update.add_subparsers(dest="update_cmd", required=True)
    update_check = update_sub.add_parser("check")
    update_check.add_argument("--local-manifest", required=True)
    update_check.set_defaults(func=cmd_update)
    update_plan = update_sub.add_parser("plan")
    update_plan.add_argument("--local-manifest", required=True)
    update_plan.set_defaults(func=cmd_update)

    return p


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
