#!/usr/bin/env bash
set -euo pipefail
PLAN_ID="${PLAN_ID:-free}"
python3 - <<PY
from zai_coder.billing_usage_enforcement.routes import route_overage_alerts
print(route_overage_alerts("${PLAN_ID}"))
PY
