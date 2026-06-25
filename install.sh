#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

mkdir -p "$HOME/.zai-coder"
if [ ! -f "$HOME/.zai-coder/config.json" ]; then
  cp config/default.config.json "$HOME/.zai-coder/config.json"
  echo "Created $HOME/.zai-coder/config.json"
else
  echo "Config exists: $HOME/.zai-coder/config.json"
fi

chmod +x ./zai-coder scripts/*.sh 2>/dev/null || true
python3 -m unittest discover -s tests -v

echo
echo "ZAI Coder installed. Try:"
echo "  ./zai-coder doctor"
echo "  ./zai-coder ask \"say hi\""
