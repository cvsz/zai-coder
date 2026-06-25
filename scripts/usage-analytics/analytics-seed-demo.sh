#!/usr/bin/env bash
set -euo pipefail
APPLY="${APPLY:-0}"
if [ "$APPLY" != "1" ]; then
  echo "DRY-RUN: set APPLY=1 to write local demo usage events."
  exit 0
fi
python3 - <<'PY'
from zai_coder.usage_analytics_insights.routes import route_analytics_seed_demo
print(route_analytics_seed_demo())
PY
