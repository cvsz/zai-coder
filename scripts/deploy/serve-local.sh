#!/usr/bin/env bash
set -euo pipefail
HOST="${HOST:-127.0.0.1}"
PORT="${PORT:-8765}"
python3 -c "from zai_coder.deployment_core.server.app import run_server; run_server('$HOST', int('$PORT'))"
