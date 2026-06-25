#!/usr/bin/env bash
set -euo pipefail
python3 - <<'PY'
from zai_coder.agent_runtime_supervisor.routes import route_agent_sandbox_profiles, route_agent_sandbox_decision
print(route_agent_sandbox_profiles())
print(route_agent_sandbox_decision())
PY
