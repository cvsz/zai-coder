# ZAI Coder TUI Template System

The ZAI Coder TUI Template System is a local-first, dry-run-first operator interface for the existing CLI. It ships six production templates with shared state, a safe command palette, and optional Textual rendering.

## Templates

- `tui-template-01` / `command-center`: focused chat, command execution, and deep-work layout.
- `tui-template-02` / `agent-hub`: multi-agent operator dashboard.
- `tui-template-03` / `flow-stream`: chronological event and command timeline.
- `tui-template-04` / `architect-tree`: hierarchical map of agents, skills, commands, docs, tests, release, and dependencies.
- `tui-template-05` / `creative-canvas`: preview-heavy workspace for docs, prompts, screenshots, and generated artifacts.
- `tui-template-06` / `operation-gate`: approval and release-gate workflow surface.

## Local Usage

```bash
./run.sh tui --dry-run
./run.sh tui --print-config
./run.sh tui --list-templates
./run.sh tui --template command-center --dry-run
./run.sh tui --template operation-gate --dry-run
```

Real Textual mode requires the optional dependency in a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[tui]"
./run.sh tui
```

Alternatively:

```bash
pipx install .
```

## Configuration

The TUI reads `config/zai-coder.config.json` when present and falls back to:

```json
{
  "enabled": true,
  "template": "command-center",
  "dry_run_first": true,
  "refresh_interval_seconds": 1,
  "show_logs": true,
  "show_agent_grid": true,
  "persist_state": true,
  "state_path": ".zai-coder/tui-state.json",
  "theme": "zeaz-glass-dark"
}
```

State persists to `.zai-coder/tui-state.json` and includes the active template, last focus, dry-run mode, last command, and log buffer. Persistence failures warn to stderr and do not crash the CLI.
