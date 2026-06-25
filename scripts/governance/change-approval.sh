#!/usr/bin/env bash
set -euo pipefail
python3 - <<'PY'
from zai_coder.enterprise_governance.routes import route_change_approval
print(route_change_approval())
PY
