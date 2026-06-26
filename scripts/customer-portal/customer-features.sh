#!/usr/bin/env bash
set -euo pipefail
PLAN="${PLAN:-free}"
python3 - <<PY
from zai_coder.customer_portal_onboarding.routes import route_customer_features
print(route_customer_features("${PLAN}"))
PY
