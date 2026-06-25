#!/usr/bin/env bash
set -euo pipefail
python3 - <<'PY'
from zai_coder.observability_suite.routes import route_slo_templates
print(route_slo_templates())
PY
