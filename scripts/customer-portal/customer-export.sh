#!/usr/bin/env bash
set -euo pipefail
APPLY="${APPLY:-0}"
if [ "$APPLY" != "1" ]; then
  echo "DRY-RUN: set APPLY=1 to write customer export bundle."
  exit 0
fi
python3 - <<'PY'
from zai_coder.customer_portal_onboarding.routes import route_customer_export
print(route_customer_export()["path"])
PY
