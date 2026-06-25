#!/usr/bin/env bash
set -euo pipefail
APPLY="${APPLY:-0}"
if [ "$APPLY" != "1" ]; then
  echo "DRY-RUN: set APPLY=1 to write demo healing plan and postmortem files."
  exit 0
fi
python3 - <<'PY'
from zai_coder.self_healing_operations.routes import route_healing_plan_demo
print(route_healing_plan_demo())
PY
