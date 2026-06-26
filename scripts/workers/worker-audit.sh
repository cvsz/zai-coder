#!/usr/bin/env bash
set -euo pipefail
python3 - <<'PY'
from zai_coder.worker_orchestration.routes import route_worker_audit
print(route_worker_audit())
PY
