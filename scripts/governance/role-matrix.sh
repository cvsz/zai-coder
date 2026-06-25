#!/usr/bin/env bash
set -euo pipefail
python3 - <<'PY'
from zai_coder.enterprise_governance.routes import route_role_matrix
print(route_role_matrix())
PY
