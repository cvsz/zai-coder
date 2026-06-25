#!/usr/bin/env bash
set -euo pipefail
ORG_ID="${ORG_ID:-org_local}"
python3 - <<PY
from zai_coder.payment_provider_sandbox.routes import route_webhook_draft, route_webhook_policy
print(route_webhook_draft("${ORG_ID}"))
print(route_webhook_policy())
PY
