#!/usr/bin/env bash
set -euo pipefail
PLAN_ID="${PLAN_ID:-free}"
python3 - <<PY
from zai_coder.billing_usage_enforcement.routes import route_plan_policy
print(route_plan_policy("${PLAN_ID}"))
PY
