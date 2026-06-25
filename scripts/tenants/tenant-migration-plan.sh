#!/usr/bin/env bash
set -euo pipefail
python3 - <<'PY'
from zai_coder.multi_tenant_control.routes import route_tenant_migration_plan
print(route_tenant_migration_plan())
PY
