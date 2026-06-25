#!/usr/bin/env bash
set -euo pipefail
PROVIDER="${PROVIDER:-github}"
APPLY="${APPLY:-0}"
python3 - <<PY
from zai_coder.multi_tenant_control.routes import route_provider_permission
print(route_provider_permission({"provider":"${PROVIDER}", "apply": "${APPLY}" == "1"}))
PY
