#!/usr/bin/env bash
set -euo pipefail
python3 - <<'PY'
from zai_coder.execution_runner.routes import route_execution_status
print(route_execution_status())
PY
