#!/usr/bin/env bash
set -euo pipefail
APPLY="${APPLY:-0}"
if [ "$APPLY" != "1" ]; then
  echo "DRY-RUN: set APPLY=1 to create demo agent task in local SQLite."
  exit 0
fi
python3 - <<'PY'
from zai_coder.agent_runtime_supervisor.routes import route_agent_assign_task_demo
print(route_agent_assign_task_demo())
PY
