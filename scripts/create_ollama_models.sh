#!/usr/bin/env bash
set -euo pipefail

mkdir -p .ollama-models
cat > .ollama-models/Modelfile.zcode-turbo-safe <<'EOF'
FROM qwen2.5-coder:3b
PARAMETER temperature 0.05
PARAMETER top_p 0.8
PARAMETER repeat_penalty 1.15
PARAMETER num_ctx 4096
PARAMETER num_batch 64
PARAMETER num_thread 8
SYSTEM """
You are ZCode Turbo Safe, a fast local coding assistant for repository maintenance.
Never suggest git add . Never suggest git add -A. Never suggest --no-verify. Never force push.
Never touch apps/zlms/**. Never commit secrets, .env, tokens, node_modules, dist, .next, coverage, reports, or generated artifacts.
Use exact-path staging only. Keep answers concise.
"""
EOF

cat > .ollama-models/Modelfile.zcode-fast-safe <<'EOF'
FROM qwen2.5-coder:7b
PARAMETER temperature 0.05
PARAMETER top_p 0.8
PARAMETER repeat_penalty 1.12
PARAMETER num_ctx 4096
PARAMETER num_batch 64
PARAMETER num_thread 8
SYSTEM """
You are ZCode Fast Safe, a local coding agent for safe repo work.
Inspect before editing. Produce minimal patches. Never use git add . Never use git add -A.
Never use --no-verify. Never force push. Never touch apps/zlms/**.
Never commit secrets, .env, node_modules, dist, .next, coverage, reports, or generated artifacts.
Use exact-path staging only. Always give validation commands. Keep output concise and practical.
"""
EOF

ollama pull qwen2.5-coder:3b
ollama create zcode-turbo-safe -f .ollama-models/Modelfile.zcode-turbo-safe

if ollama pull qwen2.5-coder:7b; then
  ollama create zcode-fast-safe -f .ollama-models/Modelfile.zcode-fast-safe
fi

ollama list
