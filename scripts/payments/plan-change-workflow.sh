#!/usr/bin/env bash
set -euo pipefail
CURRENT_PLAN_ID="${CURRENT_PLAN_ID:-free}"
TARGET_PLAN_ID="${TARGET_PLAN_ID:-pro}"
python3 - <<PY
from zai_coder.payment_provider_sandbox.routes import route_plan_change
print(route_plan_change("${CURRENT_PLAN_ID}", "${TARGET_PLAN_ID}"))
PY
