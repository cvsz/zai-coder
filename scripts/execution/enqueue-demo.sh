#!/usr/bin/env bash
set -euo pipefail
python3 - <<'PY'
from zai_coder.execution_runner.routes import route_enqueue
print(route_enqueue({"provider":"local","action":"demo","command":["echo","hello"],"apply":False}))
PY
