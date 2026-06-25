#!/usr/bin/env bash
set -euo pipefail
python3 - <<'PY'
from zai_coder.payment_provider_sandbox.routes import route_payment_audit
print(route_payment_audit())
PY
