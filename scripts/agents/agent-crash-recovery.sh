#!/usr/bin/env bash
set -euo pipefail
python3 - <<'PY'
from zai_coder.agent_runtime_supervisor.routes import route_agent_crash_recovery
print(route_agent_crash_recovery())
PY
