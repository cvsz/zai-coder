#!/usr/bin/env bash
set -euo pipefail
python3 - <<'PY'
from zai_coder.observability_suite.routes import route_health_trends
print(route_health_trends())
PY
