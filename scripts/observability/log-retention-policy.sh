#!/usr/bin/env bash
set -euo pipefail
python3 - <<'PY'
from zai_coder.observability_suite.routes import route_log_retention
print(route_log_retention())
PY
