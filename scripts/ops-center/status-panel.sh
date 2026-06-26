#!/usr/bin/env bash
set -euo pipefail
python3 - <<'PY'
from zai_coder.operations_control_center.routes import route_ops_status, route_ops_services
print(route_ops_status())
print(route_ops_services())
PY
