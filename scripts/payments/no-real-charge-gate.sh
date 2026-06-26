#!/usr/bin/env bash
set -euo pipefail
python3 - <<'PY'
from zai_coder.payment_provider_sandbox.routes import route_no_real_charge_gate, route_payment_apply_policy
print(route_no_real_charge_gate())
print(route_payment_apply_policy())
PY
