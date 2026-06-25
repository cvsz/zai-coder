#!/usr/bin/env bash
set -euo pipefail
python3 - <<'PY'
from zai_coder.enterprise_governance.routes import route_tenant_isolation
print(route_tenant_isolation({"organization_id":"org_local","workspace_id":"ws_local","actor":"admin"}))
PY
