# ZAI Coder Standalone

ZAI Coder is a local-first, standalone AI coding and media-agent framework. It ships as plain Python source code with no mandatory third-party dependencies.

It includes:

- `zai-coder` command-line interface
- local Ollama / OpenAI-compatible model adapter
- safe command runner with destructive-command guardrails
- skill registry
- agent registry
- multi-agent orchestration core
- chat sessions
- coding planner/reviewer agents
- offline fallback media generators for images, voice, music, animation, and video storyboards
- optional Textual TUI template system for local operator workflows
- self-tests

> This package does **not** include model weights. Use it with Ollama models such as `zcode-turbo-safe`, `zcode-fast-safe`, or any OpenAI-compatible endpoint.

## Installation

### Dry-run (Preview)
```bash
make install-dry-run
```

### Real Install
```bash
make install APPLY=1
```
*(Default prefix: ~/.local/share/zai-coder)*

### Custom Path
```bash
PREFIX=/custom/path make install APPLY=1
```

### Post-Install
```bash
make post-install-check
~/.local/bin/zai-coder doctor
```

### Uninstall
```bash
make uninstall APPLY=1
```

### PATH Setup
Ensure `~/.local/bin` is in your `PATH`:
```bash
export PATH="$HOME/.local/bin:$PATH"
```


## Recommended local Ollama models

Fast:

```bash
ollama run zcode-turbo-safe
```

Balanced:

```bash
ollama run zcode-fast-safe
```

Heavy:

```bash
ollama run zcode-qwen25-coder:14b-tiny
```

## Commands

```bash
./zai-coder doctor
./zai-coder agents
./zai-coder skills
./zai-coder ask "your task" --agent coder
./zai-coder chat --agent coder
./zai-coder plan --task "fix failing tests safely"
./zai-coder run "git status --short"
./zai-coder media image --prompt "ZAI neon robot" --out out/image.svg
./zai-coder media voice --text "Hello from ZAI" --out out/voice.wav
./zai-coder media music --prompt "calm coding loop" --out out/music.wav
./zai-coder media animation --prompt "agent workflow" --out out/animation.svg
./zai-coder media video --prompt "demo launch" --out out/video_storyboard.json
```

## TUI Template System

The TUI is optional. Non-TUI CLI commands work without Textual installed.

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

python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[tui]"
./run.sh tui
```

Templates:

- `tui-template-01` / `command-center`
- `tui-template-02` / `agent-hub`
- `tui-template-03` / `flow-stream`
- `tui-template-04` / `architect-tree`
- `tui-template-05` / `creative-canvas`
- `tui-template-06` / `operation-gate`

The terminal design uses layered panels, soft borders, dim/bright contrast, status chips, a command palette, and non-blocking refresh. It does not rely on web-only backdrop blur.

Installed launcher examples:

```bash
~/.local/bin/zai-coder tui --dry-run
~/.local/bin/zai-coder tui --print-config
~/.local/bin/zai-coder tui --list-templates
~/.local/bin/zai-coder tui --template command-center --dry-run
~/.local/bin/zai-coder tui --template operation-gate --dry-run
```

TUI safety allows only local read/check commands from the registry: `./run.sh doctor`, `make safety-check`, `make final-release-status`, `make install-dry-run`, and `./run.sh tui --print-config`. It blocks external mutation, `APPLY=1`, external `curl`/`wget`, and secret-like command text.

## Safety defaults

The command runner blocks dangerous patterns by default, including:

- `git add .`
- `git add -A`
- `--no-verify`
- forced pushes
- broad `rm -rf`
- staging generated artifacts
- touching `apps/zlms/**` unless explicitly configured otherwise

Mutating Makefile workflows are dry-run by default. Use `APPLY=1` only after reviewing the command and exact target paths. No `git add .` workflow is supported; stage explicit files only.

## Config

Default config path:

```text
~/.zai-coder/config.json
```

Example:

```json
{
  "provider": "ollama",
  "base_url": "http://127.0.0.1:11434/v1",
  "model": "zcode-fast-safe",
  "fallback_models": ["zcode-turbo-safe", "zcode-qwen25-coder:14b-tiny"],
  "workspace": ".",
  "max_tokens": 2048,
  "temperature": 0.05
}
```

## Project layout

```text
zai_coder/
  agents/          agent implementations
  core/            model/session/orchestrator/tool runtime
  media/           offline media generators
  skills/          built-in skills
assets/
  agents/          registry JSON
  skills/          registry JSON
  prompts/         system prompts
examples/          sample workflows
scripts/           packaging helpers
tests/             no-dependency tests
```

## Run tests

```bash
python3 -m pytest -q
```

## License

MIT. See `LICENSE`.
