#!/usr/bin/env bash
set -euo pipefail
python3 - <<'PY'
from zai_coder.production_readiness_go_live_command_center.routes import route_rollback_plan
print(route_rollback_plan())
PY
