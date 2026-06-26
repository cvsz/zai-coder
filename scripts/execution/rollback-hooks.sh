#!/usr/bin/env bash
set -euo pipefail
python3 - <<'PY'
from zai_coder.execution_runner.routes import route_rollback_hooks
print(route_rollback_hooks())
PY
