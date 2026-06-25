#!/usr/bin/env bash
set -euo pipefail
python3 - <<'PY'
from zai_coder.operations_control_center.routes import (
    route_ops_service_status_plan,
    route_ops_restart_plan,
    route_ops_backup,
    route_ops_upgrade,
    route_ops_rollback,
)
for fn in [route_ops_service_status_plan, route_ops_restart_plan, route_ops_backup, route_ops_upgrade, route_ops_rollback]:
    print(fn())
PY
