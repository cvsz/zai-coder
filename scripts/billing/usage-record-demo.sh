#!/usr/bin/env bash
set -euo pipefail
APPLY="${APPLY:-0}"
if [ "$APPLY" != "1" ]; then
  echo "DRY-RUN: set APPLY=1 to record demo usage event."
  exit 0
fi
python3 - <<'PY'
from zai_coder.billing_usage_enforcement.routes import route_record_usage_demo
print(route_record_usage_demo())
PY
