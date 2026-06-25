#!/usr/bin/env bash
set -euo pipefail
python3 - <<'PY'
from zai_coder.multi_tenant_control.routes import route_tenant_onboarding_plan
print(route_tenant_onboarding_plan())
PY
