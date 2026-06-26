# ZAI Coder TUI Template System

The ZAI Coder TUI Template System is a local-first, dry-run-first operator interface for the existing CLI. It ships six production templates with shared state, a safe command palette, and optional Textual rendering.

Implementation status: real source implementation. The templates are registered Python classes with metadata, static terminal previews, shared state, safe action dispatch, and a lazy Textual launch path. Textual is never imported by non-TUI commands.

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
./run.sh tui --template agent-hub --dry-run
./run.sh tui --template flow-stream --dry-run
./run.sh tui --template architect-tree --dry-run
./run.sh tui --template creative-canvas --dry-run
./run.sh tui --template operation-gate --dry-run
./run.sh tui --template operation-gate --no-textual
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

Installed launcher usage:

```bash
~/.local/bin/zai-coder tui --dry-run
~/.local/bin/zai-coder tui --print-config
~/.local/bin/zai-coder tui --list-templates
~/.local/bin/zai-coder tui --template command-center --dry-run
~/.local/bin/zai-coder tui --template operation-gate --dry-run
```

Make targets:

```bash
make tui
make tui-dry-run
make tui-check
make tui-command-center
make tui-agent-hub
make tui-flow-stream
make tui-architect-tree
make tui-creative-canvas
make tui-operation-gate
```

## Architecture

- `zai_coder/tui/config.py`: typed `TuiConfig`, default fallback, config-file resolution, and template validation.
- `zai_coder/tui/loader.py`: route aliases, `TemplateInfo`, template class loading, and instance creation.
- `zai_coder/tui/state.py`: shared state models, redacted log appends, template switching, JSON conversion, and persistence helpers.
- `zai_coder/tui/navigation.py`: command palette entries, help metadata, and template navigation.
- `zai_coder/tui/actions.py`: safe local action registry and typed execution result.
- `zai_coder/tui/safety.py`: allowlist, blocklist, dry-run-first checks, and secret redaction.
- `zai_coder/tui/app.py`: JSON launch plan, static preview, and lazy Textual app factory.
- `zai_coder/tui/templates/`: six concrete template classes using shared metadata and state.

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

State persists to `.zai-coder/tui-state.json` and includes active template, last focus, dry-run mode, last command, last result, log buffer, agent tiles, timeline events, and gate statuses. Persistence failures warn to stderr and do not crash the CLI. Secret-like output is redacted before saving.

## Troubleshooting

- Missing Textual: create a virtual environment and install `.[tui]`; do not install into system Python on Ubuntu 24.04.
- Invalid template: run `./run.sh tui --list-templates` and use one of the listed names or route IDs.
- State issues: remove `.zai-coder/tui-state.json`; the next run recreates default state.
- Safety block: run `./run.sh tui --dry-run` or use only the allowed command registry in `docs/tui/safety.md`.

## Release Validation Checklist

```bash
python3 -m pytest -q
make test
make safety-check
make tui-check
make install APPLY=1
make post-install-check
~/.local/bin/zai-coder tui --dry-run
~/.local/bin/zai-coder tui --print-config
~/.local/bin/zai-coder tui --list-templates
```
