from __future__ import annotations

import json
import os
import platform
import shutil
import subprocess
import sys
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True)
class SelfFeature:
    name: str
    category: str
    maturity: str
    mutation: bool
    description: str
    commands: tuple[str, ...]
    outputs: tuple[str, ...]
    safety: tuple[str, ...]


SELF_FEATURES: tuple[SelfFeature, ...] = (
    SelfFeature(
        "self-doctor", "diagnostics", "ready", False,
        "Run local health checks for Python, package files, config, Ollama, disk, and safe command policy.",
        ("./zai-coder self doctor", "make self-doctor"),
        ("terminal report", "audit event"),
        ("read-only", "no network required"),
    ),
    SelfFeature(
        "self-test", "quality", "ready", False,
        "Run unit tests and summarize failures without modifying source files.",
        ("make test", "python3 -m pytest -q"),
        ("pytest report",),
        ("dry-run by default through Makefile",),
    ),
    SelfFeature(
        "self-lint", "quality", "planned", False,
        "Run lightweight syntax and style checks with compileall and optional linters when installed.",
        ("make compile", "./zai-coder self runbook self-lint"),
        ("lint report",),
        ("read-only",),
    ),
    SelfFeature(
        "self-scan", "intelligence", "ready", False,
        "Scan project structure while ignoring generated and protected paths.",
        ("./zai-coder scan", "make scan"),
        ("project markdown/json summary",),
        ("blocks apps/zlms/** by default", "ignores generated artifacts"),
    ),
    SelfFeature(
        "self-index", "intelligence", "next", False,
        "Build a local file and symbol index for fast project navigation.",
        ("./zai-coder index build",),
        ("SQLite file index", "symbol table"),
        ("no generated paths", "no secrets indexing"),
    ),
    SelfFeature(
        "self-rag", "intelligence", "next", False,
        "Build local retrieval context from project chunks and memory.",
        ("./zai-coder rag build", "./zai-coder ask --with-rag ..."),
        ("chunk table", "retrieval results"),
        ("local-first", "redact secrets before storing chunks"),
    ),
    SelfFeature(
        "self-plan", "orchestration", "ready", False,
        "Generate a safe implementation plan before edits.",
        ("./zai-coder self plan", "./zai-coder plan --task ..."),
        ("markdown plan",),
        ("no mutation",),
    ),
    SelfFeature(
        "self-orchestrate", "orchestration", "next", False,
        "Coordinate planner, coder, reviewer, tester, security, and docs agents.",
        ("./zai-coder task create --agent supervisor",),
        ("task graph", "agent logs"),
        ("approval required before writes",),
    ),
    SelfFeature(
        "self-queue", "orchestration", "next", True,
        "Persist tasks with queued/running/completed/failed/cancelled states.",
        ("./zai-coder task list", "./zai-coder task logs TASK_ID"),
        ("SQLite queue", "run logs"),
        ("bounded workers", "cancel support"),
    ),
    SelfFeature(
        "self-heal", "repair", "next", True,
        "Detect failed tests or broken commands, propose minimal patches, and require approval before apply.",
        ("./zai-coder self heal --check",),
        ("fix plan", "candidate patch"),
        ("dry-run first", "checkpoint before apply", "no destructive commands"),
    ),
    SelfFeature(
        "self-repair", "repair", "next", True,
        "Apply verified patches through git apply after safety checks.",
        ("./zai-coder patch fix.diff --check", "make patch-apply PATCH=fix.diff APPLY=1"),
        ("checkpoint", "audit entry"),
        ("APPLY=1 required", "patch check before apply"),
    ),
    SelfFeature(
        "self-review", "quality", "ready", False,
        "Review plans or diffs for risks, test coverage, and repo safety rules.",
        ("./zai-coder ask 'review this diff' --agent reviewer",),
        ("review checklist",),
        ("read-only",),
    ),
    SelfFeature(
        "self-audit", "governance", "ready", False,
        "Record and inspect audit events for agent, HTTP, patch, and command activity.",
        ("./zai-coder audit --limit 50",),
        ("JSONL audit log",),
        ("redacted output", "append-only"),
    ),
    SelfFeature(
        "self-govern", "governance", "next", True,
        "Apply policy profiles for command allowlists, protected paths, and approval modes.",
        ("./zai-coder policy check",),
        ("policy decision",),
        ("deny by default for high-risk actions",),
    ),
    SelfFeature(
        "self-secure", "security", "ready", False,
        "Scan commands and paths for secrets, bypass flags, broad deletes, and generated artifacts.",
        ("./scripts/safety-check.sh .", "make safety-check"),
        ("safety report",),
        ("blocks git add .", "blocks --no-verify", "blocks secrets"),
    ),
    SelfFeature(
        "self-redact", "security", "next", False,
        "Redact tokens, API keys, and private paths before model or log storage.",
        ("./zai-coder redact FILE",),
        ("redacted text",),
        ("never print raw secrets",),
    ),
    SelfFeature(
        "self-backup", "resilience", "ready", True,
        "Create local checkpoints before patch or risky mutations.",
        ("./zai-coder checkpoint create",),
        ("checkpoint directory",),
        ("APPLY=1 for mutation", "bounded checkpoint size"),
    ),
    SelfFeature(
        "self-rollback", "resilience", "next", True,
        "Restore a previous checkpoint and audit the rollback.",
        ("./zai-coder checkpoint restore CHECKPOINT_ID",),
        ("restored files", "audit entry"),
        ("explicit checkpoint id", "confirmation required"),
    ),
    SelfFeature(
        "self-monitor", "observability", "next", False,
        "Monitor local CPU, RAM, disk, Ollama status, queue health, and recent failures.",
        ("./zai-coder self monitor",),
        ("health report",),
        ("read-only",),
    ),
    SelfFeature(
        "self-benchmark", "quality", "next", False,
        "Benchmark model latency, prompt quality, and safety-rule adherence.",
        ("./zai-coder bench models",),
        ("benchmark report",),
        ("small prompts by default",),
    ),
    SelfFeature(
        "self-evaluate", "quality", "next", False,
        "Evaluate agents against regression prompts and expected safety outcomes.",
        ("./zai-coder eval run" ,),
        ("eval scores",),
        ("no source mutation",),
    ),
    SelfFeature(
        "self-document", "docs", "ready", True,
        "Generate or update requirement docs, feature matrix, and operator runbooks.",
        ("./zai-coder self requirement-next --out docs/requirements/NEXT_SELF_REQUIREMENTS.md",),
        ("markdown docs",),
        ("explicit output path", "safe path check"),
    ),
    SelfFeature(
        "self-explain", "docs", "ready", False,
        "Explain package capabilities, commands, and next roadmap.",
        ("./zai-coder self list",),
        ("feature list",),
        ("read-only",),
    ),
    SelfFeature(
        "self-update", "maintenance", "next", True,
        "Update package scaffolds through safe patch bundles, never curl-pipe shell.",
        ("./zai-coder update check",),
        ("update plan", "patch bundle"),
        ("dry-run first", "no auto-update from remote scripts"),
    ),
    SelfFeature(
        "self-upgrade", "maintenance", "next", True,
        "Apply versioned migrations for config, memory, and task queue schemas.",
        ("./zai-coder migrate",),
        ("migration report",),
        ("backup before migration",),
    ),
    SelfFeature(
        "self-host", "deployment", "ready", True,
        "Run local API/web UI on localhost by default.",
        ("./zai-coder serve --host 127.0.0.1 --port 8765", "make serve APPLY=1"),
        ("local web UI",),
        ("localhost default", "remote bind requires auth in next phase"),
    ),
    SelfFeature(
        "self-deploy", "deployment", "next", True,
        "Generate deploy plans for systemd, Docker, and reverse proxy without mutating production by default.",
        ("./zai-coder deploy plan",),
        ("deployment checklist",),
        ("operator approval required",),
    ),
    SelfFeature(
        "self-package", "release", "ready", True,
        "Build a release ZIP after tests and safety checks.",
        ("make package APPLY=1", "./scripts/package.sh zai-coder-release"),
        ("release zip",),
        ("test before package", "no secrets"),
    ),
    SelfFeature(
        "self-clean", "maintenance", "ready", True,
        "Remove only local Python/test cache files.",
        ("make clean-preview", "make clean-safe APPLY=1"),
        ("cache cleanup report",),
        ("no project source deletion",),
    ),
    SelfFeature(
        "self-media", "media", "ready", True,
        "Generate local SVG/WAV/storyboard artifacts for image, voice, music, animation, and video planning.",
        ("./zai-coder media image --prompt ...", "./zai-coder media voice --text ..."),
        ("media artifacts",),
        ("local fallback generators",),
    ),
)


def list_self_features(category: str | None = None) -> list[SelfFeature]:
    items = list(SELF_FEATURES)
    if category:
        items = [item for item in items if item.category == category]
    return items


def feature_summary() -> dict[str, int]:
    summary: dict[str, int] = {"total": len(SELF_FEATURES), "ready": 0, "next": 0, "planned": 0, "mutating": 0, "read_only": 0}
    for item in SELF_FEATURES:
        summary[item.maturity] = summary.get(item.maturity, 0) + 1
        summary["mutating" if item.mutation else "read_only"] += 1
        summary[f"category:{item.category}"] = summary.get(f"category:{item.category}", 0) + 1
    return summary


def self_features_markdown(category: str | None = None) -> str:
    items = list_self_features(category)
    lines = ["# ZAI Coder self-* Feature Matrix", "", f"Total features: **{len(items)}**", "", "| Feature | Category | Maturity | Mutation | Description |", "|---|---|---|---:|---|"]
    for item in items:
        lines.append(f"| `{item.name}` | {item.category} | {item.maturity} | {'yes' if item.mutation else 'no'} | {item.description} |")
    return "\n".join(lines) + "\n"


def next_requirements_markdown() -> str:
    ready = [f for f in SELF_FEATURES if f.maturity == "ready"]
    next_items = [f for f in SELF_FEATURES if f.maturity in {"next", "planned"}]
    lines = [
        "# ZAI Coder Next Requirements: all self-* systems",
        "",
        "Target package: `zai-coder-control-plane-v2-self.zip`",
        "",
        "## Goals",
        "",
        "- Keep local-first operation as the default.",
        "- Make every risky action dry-run-first.",
        "- Add self-diagnostics, self-repair, self-monitoring, self-documentation, self-hosting, self-packaging, and self-governance.",
        "- Preserve hard safety rules: no `git add .`, no `git add -A`, no `--no-verify`, no force push, no `apps/zlms/**`, no secrets, no generated artifacts.",
        "",
        "## Baseline ready self-* features",
        "",
    ]
    for feature in ready:
        lines.append(f"- `{feature.name}` — {feature.description}")
    lines += ["", "## Next implementation requirements", ""]
    grouped: dict[str, list[SelfFeature]] = {}
    for feature in next_items:
        grouped.setdefault(feature.category, []).append(feature)
    for category, features in sorted(grouped.items()):
        lines += [f"### {category}", ""]
        for feature in features:
            lines.append(f"- `{feature.name}`")
            lines.append(f"  - Requirement: {feature.description}")
            lines.append(f"  - Commands: {', '.join(f'`{c}`' for c in feature.commands)}")
            lines.append(f"  - Outputs: {', '.join(feature.outputs)}")
            lines.append(f"  - Safety: {', '.join(feature.safety)}")
        lines.append("")
    lines += [
        "## Acceptance checks",
        "",
        "```bash",
        "make doctor",
        "make self-list",
        "make self-plan",
        "make self-requirement-next",
        "make test",
        "make safety-check",
        "```",
        "",
        "Expected: all tests pass, unsafe commands remain blocked, generated requirement docs contain every self-* feature.",
        "",
    ]
    return "\n".join(lines)


def run_self_doctor(root: Path | str = ".") -> dict[str, object]:
    root = Path(root).resolve()
    py_files = list(root.glob("zai_coder/**/*.py"))
    report: dict[str, object] = {
        "ok": True,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "root": str(root),
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "features": feature_summary(),
        "files": {
            "python": len(py_files),
            "tests": len(list(root.glob("tests/test_*.py"))),
            "agents": len(list((root / "assets" / "agents").glob("*.json"))) if (root / "assets" / "agents").exists() else 0,
            "skills": len(list((root / "assets" / "skills").glob("*.json"))) if (root / "assets" / "skills").exists() else 0,
        },
        "tools": {
            "git": bool(shutil.which("git")),
            "ollama": bool(shutil.which("ollama")),
            "pytest": bool(shutil.which("pytest")),
        },
    }
    required = ["zai_coder/cli.py", "zai_coder/core/safety.py", "Makefile", "scripts/safety-dry-run.sh"]
    missing = [p for p in required if not (root / p).exists()]
    report["missing"] = missing
    report["ok"] = not missing
    return report


def runbook(feature_name: str) -> str:
    features = {feature.name: feature for feature in SELF_FEATURES}
    if feature_name not in features:
        known = ", ".join(sorted(features))
        raise KeyError(f"Unknown self feature: {feature_name}. Known: {known}")
    feature = features[feature_name]
    lines = [f"# Runbook: {feature.name}", "", feature.description, "", "## Commands", ""]
    for command in feature.commands:
        lines.append(f"```bash\n{command}\n```")
    lines += ["", "## Outputs", ""]
    for output in feature.outputs:
        lines.append(f"- {output}")
    lines += ["", "## Safety", ""]
    for safety in feature.safety:
        lines.append(f"- {safety}")
    return "\n".join(lines) + "\n"


def write_text_safely(out_path: str | Path, content: str, workspace: str | Path = ".") -> Path:
    from .safety import SafetyPolicy

    workspace = Path(workspace).resolve()
    out = Path(out_path).expanduser()
    if not out.is_absolute():
        out = workspace / out
    out = out.resolve()
    if not str(out).startswith(str(workspace)):
        raise ValueError("Output path must stay inside workspace")
    rel = str(out.relative_to(workspace))
    check = SafetyPolicy().check_path(rel)
    if not check.allowed:
        raise ValueError(check.reason)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(content, encoding="utf-8")
    return out


def features_json() -> str:
    return json.dumps([asdict(f) for f in SELF_FEATURES], indent=2, ensure_ascii=False)
