#!/usr/bin/env bash
set -euo pipefail
python3 - <<'PY'
from zai_coder.enterprise_sso_identity_center.routes import route_sso_plan
print(route_sso_plan())
PY
