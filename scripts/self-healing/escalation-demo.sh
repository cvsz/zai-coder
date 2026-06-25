#!/usr/bin/env bash
set -euo pipefail
python3 - <<'PY'
from zai_coder.self_healing_operations.routes import route_escalation_demo
print(route_escalation_demo())
PY
