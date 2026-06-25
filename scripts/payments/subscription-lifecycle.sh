#!/usr/bin/env bash
set -euo pipefail
python3 - <<'PY'
from zai_coder.payment_provider_sandbox.routes import route_subscription_lifecycle
print(route_subscription_lifecycle())
PY
