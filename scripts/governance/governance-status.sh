#!/usr/bin/env bash
set -euo pipefail
python3 - <<'PY'
from zai_coder.enterprise_governance.routes import route_governance_status
print(route_governance_status())
PY
