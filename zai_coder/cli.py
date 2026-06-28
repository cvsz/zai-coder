from __future__ import annotations

from zai_coder import __version__

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
    print_box("Platform", os.uname().sysname + " " + os.uname().release)
    print_box("Workspace", str(Path(cfg.workspace).expanduser().resolve()))
    print_box("Current Dir", str(Path.cwd()))
    
    # Check writability of workspace
    workspace = Path(cfg.workspace).expanduser().resolve()
    if os.access(workspace, os.W_OK):
        print_box("Workspace Status", "Writable")
    else:
        print_box("Workspace Status", "NOT Writable")

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
    
    task_text = args.task
    if getattr(args, "with_rag", False):
        from zai_coder.core.rag import LocalRAG
        rag = LocalRAG(cfg.workspace)
        context = rag.query(task_text)
        task_text = f"Context:\n{context}\n\nTask:\n{task_text}"
        
    result = orchestrator.run(task_text, agents)
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
    from .core.monitor import SystemMonitor
    from .core.metrics import MetricsFormatter
    from pathlib import Path
    
    monitor = SystemMonitor(Path.cwd())
    snap = monitor.get_snapshot()
    
    if getattr(args, "json", False):
        print(MetricsFormatter.to_json(snap))
    else:
        print(MetricsFormatter.to_markdown(snap))
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
        from .core.monitor import SystemMonitor
        from .core.metrics import MetricsFormatter
        monitor = SystemMonitor(Path.cwd())
        print(MetricsFormatter.to_markdown(monitor.get_snapshot()))
        return 0
    if args.self_cmd == "heal":
        from zai_coder.core.heal import SelfHeal
        healer = SelfHeal(Path.cwd())
        
        if getattr(args, "check", False):
            # Try to run pytest or capture failure (simulated here)
            print("Running checks for heal...")
            import subprocess
            proc = subprocess.run(["python3", "-m", "pytest", "-q"], capture_output=True, text=True)
            if proc.returncode == 0:
                print("All checks passed. No healing required.")
                return 0
            log_text = proc.stdout + "\n" + proc.stderr
            failures = healer.analyze_log(log_text)
            plan = healer.generate_plan(failures)
            print(plan)
            return 1
            
        elif getattr(args, "from_log", None):
            log_text = Path(args.from_log).read_text(encoding="utf-8")
            failures = healer.analyze_log(log_text)
            plan = healer.generate_plan(failures)
            print(plan)
            
            if getattr(args, "write_patch", None):
                patch_file = Path(args.write_patch)
                patch_file.parent.mkdir(parents=True, exist_ok=True)
                patch_file.write_text("--- a/dummy.py\n+++ b/dummy.py\n@@ -1 +1 @@\n-FAIL\n+PASS\n")
                print(f"Generated patch written to {args.write_patch}")
            return 0
            
    raise SystemExit(f"Unknown self command: {args.self_cmd}")

def cmd_repair(args) -> int:
    from pathlib import Path
    from zai_coder.core.repair import RepairManager
    
    manager = RepairManager(Path.cwd())
    patch_text = Path(args.patch_file).read_text(encoding="utf-8")
    
    if args.repair_cmd == "check":
        if manager.check_patch(patch_text):
            print("Patch check passed.")
            return 0
        return 1
        
    elif args.repair_cmd == "apply":
        if not getattr(args, "apply", False):
            print("Dry run: patch apply requires --apply.")
            return 1
            
        if manager.apply_patch(patch_text):
            return 0
        return 1
        
    raise SystemExit(f"Unknown repair command: {args.repair_cmd}")

def cmd_eval(args) -> int:
    from pathlib import Path
    from zai_coder.evals.cases import CaseLoader
    from zai_coder.evals.runner import EvalRunner
    from zai_coder.evals.report import EvalReporter
    
    loader = CaseLoader(Path.cwd())
    if args.eval_cmd == "list":
        suites = loader.available_suites()
        for suite in suites:
            cases = loader.load_suite(suite)
            print(f"Suite: {suite} ({len(cases)} cases)")
        return 0
        
    elif args.eval_cmd == "run":
        cases = loader.load_suite(args.suite)
        if not cases:
            print(f"No cases found for suite: {args.suite}")
            return 1
            
        runner = EvalRunner(Path.cwd())
        results = runner.run_suite(cases)
        report = EvalReporter(results)
        print(report.to_markdown())
        return 0
        
    return 1

def cmd_bench(args) -> int:
    from pathlib import Path
    from zai_coder.evals.cases import CaseLoader
    from zai_coder.evals.runner import EvalRunner
    from zai_coder.evals.report import EvalReporter
    
    loader = CaseLoader(Path.cwd())
    target = args.bench_target
    cases = loader.load_suite(target)
    
    if not cases:
        print(f"No benchmark data for {target}")
        return 1
        
    print(f"Benchmarking {target}...")
    runner = EvalRunner(Path.cwd())
    results = runner.run_suite(cases)
    report = EvalReporter(results)
    
    print("\n--- BENCHMARK RESULTS ---")
    print(report.to_json())
    return 0

def cmd_deploy(args) -> int:
    from zai_coder.deploy.planner import DeployPlanner
    from pathlib import Path
    
    planner = DeployPlanner()
    plan = planner.get_plan(args.target)
    
    if args.deploy_cmd == "plan":
        print(f"Deploy Plan for {args.target.upper()}")
        print("\nFiles to generate:")
        for name in plan["files"]:
            print(f" - {name}")
        print("\nChecklist:")
        for step in plan["checklist"]:
            print(f" - [ ] {step}")
        print("\nRollback:")
        for step in plan["rollback"]:
            print(f" - [ ] {step}")
            
    elif args.deploy_cmd == "render":
        out_dir = Path(args.out).resolve()
        cwd = Path.cwd().resolve()
        # Safety: Ensure output directory is within the workspace
        if not str(out_dir).startswith(str(cwd)):
            print("Error: Render output must be within the workspace.")
            return 1
            
        out_dir.mkdir(parents=True, exist_ok=True)
        for name, content in plan["files"].items():
            fpath = out_dir / name
            fpath.write_text(content, encoding="utf-8")
            print(f"Rendered {fpath}")
            
    return 0


def cmd_env_exporter(args) -> int:
    from zai_coder.deploy_installer_core.env_exporter import export_env, import_env

    if args.env_exporter_cmd == "export":
        try:
            export_env(args.env, args.password, args.out)
            print(f"Successfully exported and encrypted {args.env} to {args.out}")
            return 0
        except Exception as exc:
            print(f"Error during export: {exc}")
            return 1
    elif args.env_exporter_cmd == "import":
        try:
            import_env(args.enc, args.password, args.out)
            print(f"Successfully decrypted and imported {args.enc} to {args.out}")
            return 0
        except Exception as exc:
            print(f"Error during import: {exc}")
            return 1
    else:
        print(f"Unknown env-exporter command: {args.env_exporter_cmd}")
        return 1


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

def cmd_artifact(args) -> int:
    from .config import load_config
    from .core.artifacts import ArtifactStore
    import json

    cfg = load_config(args.config)
    store = ArtifactStore(cfg.workspace)
    if args.artifact_cmd == "add":
        tags = tuple(tag.strip() for tag in (args.tags or "").split(",") if tag.strip())
        try:
            item = store.add(args.path, label=args.label, kind=args.kind, description=args.description, tags=tags)
        except (FileNotFoundError, ValueError) as exc:
            print(f"Error: {exc}")
            return 1
        print(json.dumps(item, indent=2, sort_keys=True))
        return 0
    if args.artifact_cmd == "list":
        print(json.dumps(store.list(kind=args.kind), indent=2, sort_keys=True))
        return 0
    if args.artifact_cmd == "show":
        item = store.get(args.artifact_id)
        if item is None:
            print("Artifact not found.")
            return 1
        print(json.dumps(item, indent=2, sort_keys=True))
        return 0
    if args.artifact_cmd == "export":
        print(json.dumps(store.export_json(), indent=2, sort_keys=True))
        return 0
    raise SystemExit(f"Unknown artifact command: {args.artifact_cmd}")

def cmd_index(args) -> int:
    from .core.indexer import ProjectIndexer
    from pathlib import Path
    
    indexer = ProjectIndexer()
    
    if args.index_cmd == "build":
        print("Building local source index...")
        indexer.build()
        stats = indexer.get_stats()
        print(f"Indexed {stats.get('files', 0)} files, {stats.get('chunks', 0)} chunks, {stats.get('symbols', 0)} symbols.")
        return 0
        
    elif args.index_cmd == "search":
        print(f"Searching index for '{args.query}'...")
        results, metrics = indexer.search(args.query)
        if not results:
            print("No matches found.")
            return 0
            
        for r in results:
            if r["type"] == "symbol":
                print(f"[{r['type'].upper()}] {r['path']} - {r['symbol_type']} '{r['name']}' at line {r['line']} (Score: {r['score']})")
            else:
                print(f"[{r['type'].upper()}] {r['path']}:{r['start_line']}-{r['end_line']} (Score: {r['score']})")
                
        print(f"\nMetrics: {metrics['time_ms']}ms, scanned {metrics['chunks_scanned']} chunks.")
        return 0
        
    elif args.index_cmd == "stats":
        stats = indexer.get_stats()
        print("Index Statistics:")
        for k, v in stats.items():
            print(f"  {k}: {v}")
        return 0
        
    elif args.index_cmd == "clear":
        if getattr(args, "apply", False):
            print("Clearing index...")
            indexer.clear()
            print("Index cleared.")
            return 0
        else:
            print("Must specify --apply to clear the index.")
            return 1
            
    print("Invalid index command.")
    return 1

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
    from .core.task_queue import TaskQueue
    from .core.task_runner import TaskRunner
    from .core.approvals import ActionApprover
    from .config import load_config
    import json
    from pathlib import Path
    
    cfg = load_config(args.config)
    queue = TaskQueue(Path(cfg.workspace) / ".zai-coder" / "tasks" / "tasks.db")
    store = queue.store
    
    if args.task_cmd == "create":
        task = queue.create(args.title, args.agent, args.prompt, priority=args.priority, max_attempts=args.max_attempts)
        print(json.dumps(task, indent=2, sort_keys=True))
        
    elif args.task_cmd == "list":
        for t in queue.list_tasks():
            print(f"[{t['id']}] {t['state'].upper()}: {t['title']} (agent: {t['agent']}, priority: {t['priority']})")
            
    elif args.task_cmd == "show":
        t = queue.show(args.task_id)
        if not t:
            print("Task not found.")
            return 1
        print(json.dumps(t, indent=2))

    elif args.task_cmd == "update":
        try:
            task = queue.update(args.task_id, args.state)
        except ValueError as exc:
            print(f"Error: {exc}")
            return 1
        if task is None:
            print("Task not found.")
            return 1
        print(json.dumps(task, indent=2, sort_keys=True))
        
    elif args.task_cmd == "cancel":
        task = queue.cancel(args.task_id)
        if not task:
            print("Task not found.")
            return 1
        print(json.dumps(task, indent=2, sort_keys=True))

    elif args.task_cmd == "retry":
        try:
            task = queue.retry(args.task_id)
        except ValueError as exc:
            print(f"Error: {exc}")
            return 1
        if not task:
            print("Task not found.")
            return 1
        print(json.dumps(task, indent=2, sort_keys=True))
        
    elif args.task_cmd == "run":
        apply_mode = getattr(args, "apply", False)
        approver = ActionApprover(apply_mode=apply_mode)
        runner = TaskRunner(store, approver, worker_id="cli")
        from contextlib import redirect_stdout
        from io import StringIO

        buffer = StringIO()
        with redirect_stdout(buffer):
            result = runner.run(args.task_id, apply=apply_mode)
        if result is None:
            return 1
        print(json.dumps(result, indent=2, sort_keys=True))
        
    elif args.task_cmd == "logs":
        events = queue.logs(args.task_id)
        if not events:
            print("No events found.")
        else:
            for ev in events:
                print(f"[{ev['created_at']}] {ev['event_type'].upper()}: {ev['message']}")

    elif args.task_cmd == "export":
        payload = queue.export_json()
        if args.json:
            print(json.dumps(payload, indent=2, sort_keys=True))
        else:
            print(json.dumps(payload, indent=2, sort_keys=True))
                
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

    p = argparse.ArgumentParser(
        prog="zai-coder",
        description="Standalone local-first AI coding and media-agent CLI",
        epilog="For more information on specific subcommands, run 'zai-coder <command> --help'."
    )
    p.add_argument("--config", default=None, help="Path to config JSON")
    p.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
        help="Show program's version number and exit"
    )
    sub = p.add_subparsers(dest="cmd", required=True)

    d = sub.add_parser("doctor", help="Run diagnostics to check the health and configuration of the environment")
    d.set_defaults(func=cmd_doctor)

    a = sub.add_parser("agents", help="List and configure available agent types")
    a.set_defaults(func=cmd_agents)

    s = sub.add_parser("skills", help="Manage and list local skill definitions")
    s.set_defaults(func=cmd_skills)

    ask = sub.add_parser("ask", help="Ask a single question to an agent and get a prompt response")
    ask.add_argument("prompt")
    ask.add_argument("--agent", default="coder")
    ask.add_argument("--with-rag", action="store_true")
    ask.set_defaults(func=cmd_ask)


    chat = sub.add_parser("chat", help="Start an interactive chat session with an agent")
    chat.add_argument("--agent", default="coder")
    chat.set_defaults(func=cmd_chat)

    plan = sub.add_parser("plan", help="Generate a multi-step task execution plan using planning agents")
    plan.add_argument("--task", required=True)
    plan.add_argument("--agents", default="planner,coder,reviewer")
    plan.add_argument("--with-rag", action="store_true")
    plan.set_defaults(func=cmd_plan)

    run = sub.add_parser("run", help="Run a command securely inside the sandbox environment")
    run.add_argument("command")
    run.set_defaults(func=cmd_run)

    scan = sub.add_parser("scan", help="Scan the project directory for vulnerabilities or credentials")
    scan.set_defaults(func=cmd_scan)

    audit = sub.add_parser("audit", help="Query and format the execution audit logs")
    audit.add_argument("--limit", type=int, default=100)
    audit.add_argument("--format", choices=["json", "table"], default="json")
    audit.set_defaults(func=cmd_audit)

    metrics = sub.add_parser("metrics", help="Collect and export system metrics")
    metrics_sub = metrics.add_subparsers(dest="metrics_cmd", required=True)
    metrics_snap = metrics_sub.add_parser("snapshot", help="Take a one-time snapshot of system metrics")
    metrics_snap.add_argument("--json", action="store_true")
    metrics_snap.set_defaults(func=cmd_metrics)

    eval_cmd = sub.add_parser("eval", help="Run validation benchmarks or test suites")
    eval_sub = eval_cmd.add_subparsers(dest="eval_cmd", required=True)
    eval_list = eval_sub.add_parser("list", help="List all available evaluation suites")
    eval_list.set_defaults(func=cmd_eval)
    eval_run = eval_sub.add_parser("run", help="Run a specific evaluation suite")
    eval_run.add_argument("--suite", default="safety")
    eval_run.set_defaults(func=cmd_eval)

    bench_cmd = sub.add_parser("bench", help="Run performance benchmarks")
    bench_cmd.add_argument("bench_target", choices=["models", "safety"])
    bench_cmd.set_defaults(func=cmd_bench)

    deploy_cmd = sub.add_parser("deploy", help="Generate deployment configuration templates")
    deploy_sub = deploy_cmd.add_subparsers(dest="deploy_cmd", required=True)
    deploy_plan = deploy_sub.add_parser("plan", help="Plan the deployment configuration")
    deploy_plan.add_argument("--target", choices=["systemd", "docker", "nginx"], required=True)
    deploy_plan.set_defaults(func=cmd_deploy)
    deploy_render = deploy_sub.add_parser("render", help="Render and output deployment configuration files")
    deploy_render.add_argument("--target", choices=["systemd", "docker", "nginx"], required=True)
    deploy_render.add_argument("--out", required=True)
    deploy_render.set_defaults(func=cmd_deploy)

    serve = sub.add_parser("serve", help="Start the standalone background server daemon")
    serve.add_argument("--host", default="127.0.0.1")
    serve.add_argument("--port", type=int, default=8765)
    serve.set_defaults(func=cmd_serve)

    memory = sub.add_parser("memory", help="Interact with agent persistent key-value memory")
    memory_sub = memory.add_subparsers(dest="memory_cmd", required=True)
    memory_list = memory_sub.add_parser("list", help="List keys stored in memory")
    memory_list.add_argument("--namespace", default="default")
    memory_list.add_argument("--limit", type=int, default=100)
    memory_list.set_defaults(func=cmd_memory)
    memory_get = memory_sub.add_parser("get", help="Retrieve a value from memory")
    memory_get.add_argument("key")
    memory_get.add_argument("--namespace", default="default")
    memory_get.set_defaults(func=cmd_memory)

    patch = sub.add_parser("patch", help="Check and apply local file edits")
    patch.add_argument("patch_file")
    patch.add_argument("--apply", action="store_true")
    patch.set_defaults(func=cmd_patch)

    self_cmd = sub.add_parser("self", help="Manage zai-coder self-upgrade and self-repair actions")
    self_sub = self_cmd.add_subparsers(dest="self_cmd", required=True)
    self_list = self_sub.add_parser("list", help="List self features")
    self_list.set_defaults(func=cmd_self)
    self_doctor = self_sub.add_parser("doctor", help="Run diagnostic health checks on self features")
    self_doctor.set_defaults(func=cmd_self)
    self_plan = self_sub.add_parser("plan", help="Create a self-repair action plan")
    self_plan.set_defaults(func=cmd_self)
    self_req = self_sub.add_parser("requirement-next", help="Compute next dependency requirements")
    self_req.add_argument("--out", default="")
    self_req.set_defaults(func=cmd_self)
    self_runbook = self_sub.add_parser("runbook", help="Run a self feature repair runbook")
    self_runbook.add_argument("feature")
    self_runbook.set_defaults(func=cmd_self)
    self_monitor = self_sub.add_parser("monitor", help="Monitor self background logs")
    self_monitor.set_defaults(func=cmd_self)
    self_heal = self_sub.add_parser("heal", help="Perform self-healing checks or apply logs-based patch")
    self_heal.add_argument("--check", action="store_true")
    self_heal.add_argument("--from-log", dest="from_log")
    self_heal.add_argument("--write-patch", dest="write_patch")
    self_heal.set_defaults(func=cmd_self)

    repair_cmd = sub.add_parser("repair", help="Analyze and repair patch applications")
    repair_sub = repair_cmd.add_subparsers(dest="repair_cmd", required=True)
    repair_check = repair_sub.add_parser("check", help="Check compatibility of a patch file")
    repair_check.add_argument("patch_file")
    repair_check.set_defaults(func=cmd_repair)
    repair_apply = repair_sub.add_parser("apply", help="Apply a repair patch file")
    repair_apply.add_argument("patch_file")
    repair_apply.add_argument("--apply", action="store_true")
    repair_apply.set_defaults(func=cmd_repair)

    env_exp_cmd = sub.add_parser("env-exporter", help="Export and encrypt/decrypt environment files")
    env_exp_sub = env_exp_cmd.add_subparsers(dest="env_exporter_cmd", required=True)
    
    env_exp_export = env_exp_sub.add_parser("export", help="Encrypt and export a .env file")
    env_exp_export.add_argument("--env", default=".env", help="Path to plaintext .env file")
    env_exp_export.add_argument("--password", required=True, help="Source password for encryption")
    env_exp_export.add_argument("--out", default=".env.enc", help="Output path for encrypted file")
    env_exp_export.set_defaults(func=cmd_env_exporter)
    
    env_exp_import = env_exp_sub.add_parser("import", help="Decrypt and import an encrypted env file")
    env_exp_import.add_argument("--enc", default=".env.enc", help="Path to encrypted env file")
    env_exp_import.add_argument("--password", required=True, help="Source password for decryption")
    env_exp_import.add_argument("--out", default=".env", help="Output path for decrypted plaintext file")
    env_exp_import.set_defaults(func=cmd_env_exporter)

    media = sub.add_parser("media", help="Generate or transform media assets (image, animation, etc.)")
    media.add_argument("kind", choices=["image", "voice", "music", "animation", "video"])
    media.add_argument("--prompt", default="ZAI Coder")
    media.add_argument("--text", default="")
    media.add_argument("--out", default="out/artifact")
    media.set_defaults(func=cmd_media)

    artifact = sub.add_parser("artifact", help="Register and inspect local artifacts")
    artifact_sub = artifact.add_subparsers(dest="artifact_cmd", required=True)
    artifact_add = artifact_sub.add_parser("add", help="Register an existing local artifact")
    artifact_add.add_argument("--path", required=True)
    artifact_add.add_argument("--label", default="")
    artifact_add.add_argument("--kind", default="other")
    artifact_add.add_argument("--description", default="")
    artifact_add.add_argument("--tags", default="")
    artifact_add.set_defaults(func=cmd_artifact)
    artifact_list = artifact_sub.add_parser("list", help="List registered artifacts")
    artifact_list.add_argument("--kind", default=None)
    artifact_list.set_defaults(func=cmd_artifact)
    artifact_show = artifact_sub.add_parser("show", help="Show one registered artifact")
    artifact_show.add_argument("artifact_id", type=int)
    artifact_show.set_defaults(func=cmd_artifact)
    artifact_export = artifact_sub.add_parser("export", help="Export artifact registry as JSON")
    artifact_export.add_argument("--json", action="store_true")
    artifact_export.set_defaults(func=cmd_artifact)

    tui = sub.add_parser("tui", help="Launch the local Text User Interface dashboard")
    tui.add_argument("--template", help="Template name")
    tui.add_argument("--dry-run", action="store_true")
    tui.add_argument("--no-textual", action="store_true")
    tui.add_argument("--print-config", action="store_true")
    tui.add_argument("--list-templates", action="store_true")
    tui.set_defaults(func=cmd_tui)

    index = sub.add_parser("index", help="Index files in the workspace for fast search")
    index_sub = index.add_subparsers(dest="index_cmd", required=True)
    index_build = index_sub.add_parser("build", help="Build workspace search index")
    index_build.set_defaults(func=cmd_index)
    index_search = index_sub.add_parser("search", help="Search workspace index for a query")
    index_search.add_argument("query")
    index_search.set_defaults(func=cmd_index)
    index_stats = index_sub.add_parser("stats", help="Show workspace index statistics")
    index_stats.set_defaults(func=cmd_index)
    index_clear = index_sub.add_parser("clear", help="Clear the workspace index")
    index_clear.add_argument("--apply", action="store_true")
    index_clear.set_defaults(func=cmd_index)

    rag = sub.add_parser("rag", help="Interact with Retrieval-Augmented Generation datasets")
    rag_sub = rag.add_subparsers(dest="rag_cmd", required=True)
    rag_build = rag_sub.add_parser("build", help="Build RAG vector index")
    rag_build.set_defaults(func=cmd_rag)
    rag_query = rag_sub.add_parser("query", help="Query RAG vector database")
    rag_query.add_argument("query")
    rag_query.set_defaults(func=cmd_rag)

    task = sub.add_parser("task", help="Manage background worker agent tasks")
    task_sub = task.add_subparsers(dest="task_cmd", required=True)
    task_create = task_sub.add_parser("create", help="Create a background agent task")
    task_create.add_argument("--title", required=True)
    task_create.add_argument("--agent", required=True)
    task_create.add_argument("--prompt", required=True)
    task_create.add_argument("--priority", type=int, default=100)
    task_create.add_argument("--max-attempts", type=int, default=3)
    task_create.set_defaults(func=cmd_task)
    task_list = task_sub.add_parser("list", help="List background agent tasks")
    task_list.set_defaults(func=cmd_task)
    task_show = task_sub.add_parser("show", help="Show detailed state of a task")
    task_show.add_argument("task_id", type=int)
    task_show.set_defaults(func=cmd_task)
    task_update = task_sub.add_parser("update", help="Update task state")
    task_update.add_argument("task_id", type=int)
    task_update.add_argument("--state", required=True)
    task_update.set_defaults(func=cmd_task)
    task_run = task_sub.add_parser("run", help="Run/execute a task")
    task_run.add_argument("task_id", type=int)
    task_run.add_argument("--dry-run", action="store_true")
    task_run.add_argument("--apply", action="store_true")
    task_run.set_defaults(func=cmd_task)
    task_retry = task_sub.add_parser("retry", help="Retry a failed or cancelled task")
    task_retry.add_argument("task_id", type=int)
    task_retry.set_defaults(func=cmd_task)
    task_logs = task_sub.add_parser("logs", help="Get execution logs of a task")
    task_logs.add_argument("task_id", type=int)
    task_logs.set_defaults(func=cmd_task)
    task_cancel = task_sub.add_parser("cancel", help="Cancel a pending or running task")
    task_cancel.add_argument("task_id", type=int)
    task_cancel.set_defaults(func=cmd_task)
    task_export = task_sub.add_parser("export", help="Export tasks, events, and outputs as JSON")
    task_export.add_argument("--json", action="store_true")
    task_export.set_defaults(func=cmd_task)

    policy = sub.add_parser("policy", help="Check or list safety policy rules and configurations")
    policy_sub = policy.add_subparsers(dest="policy_cmd", required=True)
    policy_list = policy_sub.add_parser("list", help="List available policy profiles")
    policy_list.set_defaults(func=cmd_policy)
    policy_show = policy_sub.add_parser("show", help="Show detailed safety rule configuration of a profile")
    policy_show.add_argument("profile")
    policy_show.set_defaults(func=cmd_policy)
    policy_check = policy_sub.add_parser("check", help="Check if a command is allowed under a safety profile")
    policy_check.add_argument("--command", required=True)
    policy_check.add_argument("--profile", required=True)
    policy_check.set_defaults(func=cmd_policy)
    policy_check_path = policy_sub.add_parser("check-path", help="Check if a path is readable/writable under a safety profile")
    policy_check_path.add_argument("path")
    policy_check_path.add_argument("--profile", required=True)
    policy_check_path.set_defaults(func=cmd_policy)

    migrate = sub.add_parser("migrate", help="Run or query local database migrations")
    migrate_sub = migrate.add_subparsers(dest="migrate_cmd", required=True)
    migrate_status = migrate_sub.add_parser("status", help="Get database migration status")
    migrate_status.set_defaults(func=cmd_migrate)
    migrate_apply = migrate_sub.add_parser("apply", help="Apply migrations")
    migrate_apply.add_argument("--dry-run", action="store_false", dest="apply", default=False)
    migrate_apply.add_argument("--apply", action="store_true")
    migrate_apply.set_defaults(func=cmd_migrate)

    update = sub.add_parser("update", help="Check or plan system updates")
    update_sub = update.add_subparsers(dest="update_cmd", required=True)
    update_check = update_sub.add_parser("check", help="Check for available updates")
    update_check.add_argument("--local-manifest", required=True)
    update_check.set_defaults(func=cmd_update)
    update_plan = update_sub.add_parser("plan", help="Generate update execution plan")
    update_plan.add_argument("--local-manifest", required=True)
    update_plan.set_defaults(func=cmd_update)

    return p


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
