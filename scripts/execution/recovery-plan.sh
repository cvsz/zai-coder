#!/usr/bin/env bash
set -euo pipefail
PROVIDER="${PROVIDER:-local}"
ACTION="${ACTION:-unknown}"
python3 - <<PY
from zai_coder.execution_runner.routes import route_recovery_plan
print(route_recovery_plan("${PROVIDER}", "${ACTION}", "failed"))
PY
