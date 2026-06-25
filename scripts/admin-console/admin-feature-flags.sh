#!/usr/bin/env bash
set -euo pipefail
python3 - <<'PY'
from zai_coder.enterprise_admin_console.routes import route_admin_feature_flags
print(route_admin_feature_flags())
PY
