#!/usr/bin/env bash
set -euo pipefail
HOST="${HOST:-127.0.0.1}"
PORT="${PORT:-8765}"
APP="${APP:-zai_coder.production_hardening_core.server.asgi:app}"
echo "Serving $APP on $HOST:$PORT"
exec uvicorn "$APP" --host "$HOST" --port "$PORT" --proxy-headers
