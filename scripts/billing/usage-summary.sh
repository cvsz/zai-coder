#!/usr/bin/env bash
set -euo pipefail
python3 - <<'PY'
from zai_coder.billing_usage_enforcement.routes import route_usage_summary, route_org_usage_summary
print(route_usage_summary())
print(route_org_usage_summary())
PY
