#!/usr/bin/env bash
set -euo pipefail
PLAN_ID="${PLAN_ID:-free}"
python3 - <<PY
from zai_coder.billing_usage_enforcement.routes import route_enforcement, route_action_enforcement
print(route_enforcement("${PLAN_ID}"))
print(route_action_enforcement("${PLAN_ID}", "run"))
PY
