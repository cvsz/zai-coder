#!/usr/bin/env bash
set -euo pipefail
PROVIDER="${PROVIDER:-sandbox}"
python3 - <<PY
from zai_coder.payment_provider_sandbox.routes import route_payment_env_check
print(route_payment_env_check("${PROVIDER}"))
PY
