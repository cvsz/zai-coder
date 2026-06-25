#!/usr/bin/env bash
set -euo pipefail
APPLY="${APPLY:-0}"
if [ "$APPLY" != "1" ]; then
  echo "DRY-RUN: set APPLY=1 to register demo worker in local SQLite."
  exit 0
fi
python3 - <<'PY'
from zai_coder.worker_orchestration.routes import route_worker_register_demo
print(route_worker_register_demo())
PY
