#!/usr/bin/env bash
set -euo pipefail
ACTION="${ACTION:-start}"
python3 - <<PY
from zai_coder.agent_runtime_supervisor.routes import route_agent_lifecycle_plan
print(route_agent_lifecycle_plan("${ACTION}"))
PY
