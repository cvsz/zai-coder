#!/usr/bin/env bash
set -euo pipefail
python3 - <<'PY'
from zai_coder.billing_usage_enforcement.routes import route_billing_status
print(route_billing_status())
PY
