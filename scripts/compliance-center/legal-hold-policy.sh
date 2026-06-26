#!/usr/bin/env bash
set -euo pipefail
python3 - <<'PY'
from zai_coder.enterprise_compliance_center.routes import route_legal_hold_policy
print(route_legal_hold_policy())
PY
