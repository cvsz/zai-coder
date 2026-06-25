#!/usr/bin/env bash
set -euo pipefail
python3 - <<'PY'
from zai_coder.billing_usage_enforcement.routes import route_plan_manifest
print(route_plan_manifest())
PY
