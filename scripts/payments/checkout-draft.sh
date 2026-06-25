#!/usr/bin/env bash
set -euo pipefail
ORG_ID="${ORG_ID:-org_local}"
PLAN_ID="${PLAN_ID:-free}"
python3 - <<PY
from zai_coder.payment_provider_sandbox.routes import route_checkout_draft
print(route_checkout_draft("${ORG_ID}", "${PLAN_ID}"))
PY
