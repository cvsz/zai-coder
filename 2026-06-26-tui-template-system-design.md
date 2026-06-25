# ZAI Coder TUI Template System Design

## Summary

The TUI Template System adds six production templates to the local ZAI Coder CLI without making Textual a hard dependency. The system is keyboard-first, dry-run-first, local-first, and safe by default.

## Architecture

- `zai_coder/tui/config.py`: config loading with defaults and route alias normalization.
- `zai_coder/tui/state.py`: shared dataclass state, agent tiles, timeline events, gate statuses, and JSON persistence.
- `zai_coder/tui/loader.py`: template registry and route/name normalization.
- `zai_coder/tui/actions.py`: selectable command registry and safe execution wrapper.
- `zai_coder/tui/safety.py`: mutation blocking, dry-run-first checks, and secret redaction.
- `zai_coder/tui/app.py`: dry-run plan, static terminal preview, and optional Textual launch.

## Safety

The command palette only allows local commands that inspect or dry-run. External mutation, release publishing, force pushing, `APPLY=1`, and secret-bearing commands are blocked.

## Textual Dependency Boundary

Textual is imported only inside the real launch path. `--dry-run`, `--print-config`, `--list-templates`, and `--no-textual` work without Textual installed.

## Templates

- `command-center`: focused deep-work and command surface.
- `agent-hub`: multi-agent operations dashboard.
- `flow-stream`: chronological event timeline.
- `architect-tree`: architecture and relationship navigator.
- `creative-canvas`: preview-heavy creative workspace.
- `operation-gate`: approval and release-gate workflow.
