# ZAI Coder TUI Template System Design

## Summary

The TUI Template System adds six production templates to the local ZAI Coder CLI without making Textual a hard dependency. The system is keyboard-first, dry-run-first, local-first, and safe by default.

## Architecture

- `zai_coder/tui/config.py`: config loading with defaults and route alias normalization.
- `zai_coder/tui/state.py`: shared dataclass state, agent tiles, timeline events, gate statuses, redacted logs, and JSON persistence.
- `zai_coder/tui/loader.py`: `TemplateInfo`, template class registry, route/name normalization, and instance factory.
- `zai_coder/tui/actions.py`: selectable command registry, typed execution result, pinned repo cwd, timeout, capture, and redaction.
- `zai_coder/tui/safety.py`: mutation blocking, dry-run-first checks, external URL blocking, secret detection, and secret redaction.
- `zai_coder/tui/navigation.py`: command palette entries, template switch actions, and keyboard help metadata.
- `zai_coder/tui/app.py`: dry-run plan, static terminal preview, app factory, and optional Textual launch.

## Safety

The command palette only allows local commands that inspect or dry-run. External mutation, release publishing, force pushing, `APPLY=1`, and secret-bearing commands are blocked.

## Textual Dependency Boundary

Textual is imported only inside the real launch path. `--dry-run`, `--print-config`, `--list-templates`, and `--no-textual` work without Textual installed.

When Textual is missing, real launch prints:

```text
Textual is not installed. Install optional TUI dependencies in a virtual environment:
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[tui]"
```

## Validation

The non-interactive surface is covered by tests for config loading, invalid config, aliases, loader metadata, safety blocklist, action dry-runs, state persistence, persistence failure warnings, navigation metadata, CLI dry-run/list/config/no-textual paths, and installed launcher support.

## Templates

- `command-center`: focused deep-work and command surface.
- `agent-hub`: multi-agent operations dashboard.
- `flow-stream`: chronological event timeline.
- `architect-tree`: architecture and relationship navigator.
- `creative-canvas`: preview-heavy creative workspace.
- `operation-gate`: approval and release-gate workflow.
