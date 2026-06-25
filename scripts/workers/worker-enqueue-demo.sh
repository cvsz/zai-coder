#!/usr/bin/env bash
set -euo pipefail
APPLY="${APPLY:-0}"
if [ "$APPLY" != "1" ]; then
  echo "DRY-RUN: set APPLY=1 to enqueue demo worker job."
  exit 0
fi
python3 - <<'PY'
from zai_coder.worker_orchestration.routes import route_worker_enqueue_demo
print(route_worker_enqueue_demo())
PY
