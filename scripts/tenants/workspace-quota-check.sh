#!/usr/bin/env bash
set -euo pipefail
python3 - <<'PY'
from zai_coder.multi_tenant_control.routes import route_quota_decision
print(route_quota_decision({"usage":{"monthly_runs": 10, "storage_mb": 20, "provider_apply": 1}}))
PY
