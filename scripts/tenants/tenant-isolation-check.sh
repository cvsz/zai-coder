#!/usr/bin/env bash
set -euo pipefail
python3 - <<'PY'
from zai_coder.multi_tenant_control.routes import route_tenant_isolation_check
print(route_tenant_isolation_check())
print(route_tenant_isolation_check({"org_id":"org_a","workspace_id":"ws_a","target_org_id":"org_b","target_workspace_id":"ws_a"}))
PY
