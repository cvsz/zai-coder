#!/usr/bin/env bash
set -euo pipefail
python3 - <<'PY'
from zai_coder.agent_runtime_supervisor.routes import route_agent_budget_decision, route_agent_permission_decision
print(route_agent_budget_decision())
print(route_agent_permission_decision())
PY
