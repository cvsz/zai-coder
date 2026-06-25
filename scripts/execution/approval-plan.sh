#!/usr/bin/env bash
set -euo pipefail
python3 - <<'PY'
from zai_coder.execution_runner.routes import route_approval_plan
print(route_approval_plan())
PY
