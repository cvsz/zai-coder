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
- self-tests

> This package does **not** include model weights. Use it with Ollama models such as `zcode-turbo-safe`, `zcode-fast-safe`, or any OpenAI-compatible endpoint.

## Quick start

```bash
unzip zai-coder-standalone.zip
cd zai-coder-standalone
./install.sh
./zai-coder doctor
./zai-coder ask "Inspect this repo and make a safe plan. Do not edit files."
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
python3 -m unittest discover -s tests -v
```

## License

MIT. See `LICENSE`.
