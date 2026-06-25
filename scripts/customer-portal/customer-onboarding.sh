#!/usr/bin/env bash
set -euo pipefail
python3 - <<'PY'
from zai_coder.customer_portal_onboarding.routes import route_customer_onboarding
print(route_customer_onboarding())
PY
