#!/usr/bin/env bash
set -euo pipefail
APPLY="${APPLY:-0}"
PLAN_ID="${PLAN_ID:-free}"
if [ "$APPLY" != "1" ]; then
  echo "DRY-RUN: set APPLY=1 to write invoice draft JSON."
  exit 0
fi
python3 - <<PY
from zai_coder.billing_usage_enforcement.routes import route_invoice_write
print(route_invoice_write("${PLAN_ID}"))
PY
