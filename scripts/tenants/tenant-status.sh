#!/usr/bin/env bash
set -euo pipefail
python3 - <<'PY'
from zai_coder.multi_tenant_control.routes import route_tenant_status
print(route_tenant_status())
PY
