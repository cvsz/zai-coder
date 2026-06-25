#!/usr/bin/env bash
set -euo pipefail
python3 - <<'PY'
from zai_coder.observability_suite.routes import route_observability_status
print(route_observability_status())
PY
