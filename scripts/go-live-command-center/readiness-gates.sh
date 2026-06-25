#!/usr/bin/env bash
set -euo pipefail
python3 - <<'PY'
from zai_coder.production_readiness_go_live_command_center.routes import route_readiness_gates
print(route_readiness_gates())
PY
