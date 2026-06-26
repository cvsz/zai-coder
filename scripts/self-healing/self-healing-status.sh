#!/usr/bin/env bash
set -euo pipefail
python3 - <<'PY'
from zai_coder.self_healing_operations.routes import route_self_healing_status
print(route_self_healing_status())
PY
