#!/usr/bin/env bash
set -euo pipefail
FRAMEWORK_ID="${FRAMEWORK_ID:-soc2}"
python3 - <<PY
from zai_coder.enterprise_compliance_center.routes import route_controls
print(route_controls("${FRAMEWORK_ID}"))
PY
