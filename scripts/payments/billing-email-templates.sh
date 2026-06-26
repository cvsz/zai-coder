#!/usr/bin/env bash
set -euo pipefail
python3 - <<'PY'
from zai_coder.payment_provider_sandbox.routes import route_billing_email_templates
print(route_billing_email_templates())
PY
