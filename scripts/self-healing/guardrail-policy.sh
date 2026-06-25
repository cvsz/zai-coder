#!/usr/bin/env bash
set -euo pipefail
python3 - <<'PY'
from zai_coder.self_healing_operations.routes import route_guardrail_policy
print(route_guardrail_policy())
PY
