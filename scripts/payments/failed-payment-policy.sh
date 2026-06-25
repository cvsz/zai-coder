#!/usr/bin/env bash
set -euo pipefail
PLAN_ID="${PLAN_ID:-pro}"
python3 - <<PY
from zai_coder.payment_provider_sandbox.routes import route_failed_payment_policy
print(route_failed_payment_policy("${PLAN_ID}"))
PY
