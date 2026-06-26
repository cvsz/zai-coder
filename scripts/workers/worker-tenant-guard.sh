#!/usr/bin/env bash
set -euo pipefail
python3 - <<'PY'
from zai_coder.worker_orchestration.routes import route_worker_tenant_guard
print(route_worker_tenant_guard())
PY
