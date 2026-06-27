from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


VALID_STATUSES = {"available", "partial", "planned", "requires_integration", "do_not_claim"}
VALID_TIERS = {"Free", "Pro", "Max", "Enterprise", "Internal", "Roadmap"}


@dataclass(frozen=True)
class FeatureClaim:
    id: str
    label: str
    status: str
    tier_hint: str
    claim: str
    evidence_path: str = ""
    notes: str = ""

    def to_dict(self) -> dict[str, str]:
        return {
            "id": self.id,
            "label": self.label,
            "status": self.status,
            "tier_hint": self.tier_hint,
            "claim": self.claim,
            "evidence_path": self.evidence_path,
            "notes": self.notes,
        }


CLAUDE_CODE_FEATURES: tuple[FeatureClaim, ...] = (
    FeatureClaim("terminal_cli", "Terminal CLI", "available", "Free", "Run local coding workflows from the terminal.", "zai_coder/cli.py"),
    FeatureClaim("file_read_write_edit", "File read/write/edit", "partial", "Free", "Read, inspect, and patch local files with guarded edit flows.", "zai_coder/core/patcher.py"),
    FeatureClaim("safe_bash", "Safe shell runner", "available", "Free", "Run shell commands through local safety policy checks.", "zai_coder/core/tools.py"),
    FeatureClaim("glob_grep_search", "Glob and grep style search", "partial", "Free", "Search local project files through scan, index, and shell-backed workflows.", "zai_coder/core/indexer.py"),
    FeatureClaim("task_planning", "Task planning", "available", "Free", "Generate multi-agent implementation plans.", "zai_coder/cli.py"),
    FeatureClaim("persistent_memory", "Persistent memory", "partial", "Pro", "Store local key-value memory; CLAUDE.md-compatible auto memory is planned.", "zai_coder/core/memory.py"),
    FeatureClaim("project_instructions", "Project instructions", "partial", "Free", "Use AGENTS.md and local prompts; CLAUDE.md parity is planned.", "docs/prompts/15-toolsets-skills-context-system.md"),
    FeatureClaim("slash_commands", "Slash commands", "planned", "Roadmap", "Plan command aliases and prompt-backed actions similar to slash commands.", "", "Requires command registry UX."),
    FeatureClaim("custom_commands", "Custom commands", "planned", "Roadmap", "Plan repo-defined reusable command packs.", "", "Requires command registry and validation."),
    FeatureClaim("hooks", "Hooks", "planned", "Roadmap", "Plan lifecycle hooks for pre/post command and edit events.", "", "Needs deterministic hook runner."),
    FeatureClaim("subagents", "Subagents", "partial", "Pro", "Model agent roles and agent runtime supervision with local queue foundations.", "zai_coder/agent_runtime_supervisor"),
    FeatureClaim("skills", "Skills", "partial", "Pro", "List and package local skills; install and marketplace flows are partial.", "zai_coder/agent_marketplace_and_skills"),
    FeatureClaim("mcp", "MCP integration", "requires_integration", "Enterprise", "Requires MCP server integration, credentials, and provider configuration.", "docs/prompts/18-provider-routing-mcp-plugins.md"),
    FeatureClaim("permissions", "Permissions", "available", "Free", "Apply local command and path safety policies before mutation.", "zai_coder/core/safety.py"),
    FeatureClaim("sessions", "Sessions", "partial", "Pro", "Persist local session state; full resume/continue UX is planned.", "zai_coder/core/session.py"),
    FeatureClaim("checkpointing", "Checkpointing", "partial", "Pro", "Patch checkpoints exist; full rollback workflow is planned.", "zai_coder/core/patcher.py"),
    FeatureClaim("ide_integration", "IDE integration", "planned", "Roadmap", "Plan IDE or ACP style integration.", "", "Requires editor protocol integration."),
    FeatureClaim("sdk_headless", "SDK/headless", "partial", "Enterprise", "CLI and Python modules are callable locally; formal SDK packaging is planned.", "zai_coder/cli.py"),
    FeatureClaim("plugins", "Plugins", "partial", "Enterprise", "Plugin and connector catalogs exist; remote plugin install requires integration.", "zai_coder/plugin_connector_hub"),
    FeatureClaim("web_search_fetch", "Web search/fetch", "requires_integration", "Pro", "Requires web search provider integration or browser/MCP service.", "docs/prompts/19-media-browser-voice-vision-plan.md"),
    FeatureClaim("background_monitor", "Background monitor", "partial", "Pro", "Local system monitor exists; command-output event monitoring is planned.", "zai_coder/core/monitor.py"),
    FeatureClaim("artifacts", "Artifacts", "available", "Free", "Register local artifacts with metadata, hashes, and JSON export.", "zai_coder/core/artifacts.py"),
    FeatureClaim("output_styles", "Output styles", "planned", "Roadmap", "Plan reusable response style presets.", "", "Requires prompt/style registry."),
    FeatureClaim("enterprise_settings", "Enterprise settings", "partial", "Enterprise", "Policy and admin-console foundations exist; managed policy parity is planned.", "zai_coder/enterprise_admin_console"),
)


def features_by_status(status: str) -> list[FeatureClaim]:
    return [feature for feature in CLAUDE_CODE_FEATURES if feature.status == status]


def validate_feature_claims(features: Iterable[FeatureClaim] = CLAUDE_CODE_FEATURES) -> list[str]:
    issues: list[str] = []
    seen: set[str] = set()
    for feature in features:
        if feature.id in seen:
            issues.append(f"duplicate feature id: {feature.id}")
        seen.add(feature.id)
        if feature.status not in VALID_STATUSES:
            issues.append(f"{feature.id}: invalid status {feature.status}")
        if feature.tier_hint not in VALID_TIERS:
            issues.append(f"{feature.id}: invalid tier {feature.tier_hint}")
        if feature.status == "available" and not (feature.evidence_path or feature.notes):
            issues.append(f"{feature.id}: available features require evidence or notes")
        if feature.status == "requires_integration":
            text = f"{feature.claim} {feature.notes}".lower()
            if not any(word in text for word in ("integration", "provider", "api", "oauth", "mcp", "credentials", "service")):
                issues.append(f"{feature.id}: integration status must explain the dependency")
        if feature.status == "do_not_claim" and any(word in feature.claim.lower() for word in ("supports", "available", "ready", "run", "use")):
            issues.append(f"{feature.id}: do_not_claim claim sounds available")
    return issues


def feature_matrix_markdown(features: Iterable[FeatureClaim] = CLAUDE_CODE_FEATURES) -> str:
    lines = [
        "# Claude Code Feature Coverage",
        "",
        "| Feature | Status | Tier | Claim | Evidence |",
        "|---|---|---|---|---|",
    ]
    for feature in features:
        evidence = feature.evidence_path or feature.notes
        lines.append(f"| {feature.label} | {feature.status} | {feature.tier_hint} | {feature.claim} | {evidence} |")
    return "\n".join(lines) + "\n"

