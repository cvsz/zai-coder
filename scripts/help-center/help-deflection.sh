#!/usr/bin/env bash
set -euo pipefail
python3 - <<'PY'
from zai_coder.knowledge_base_help_center.routes import route_help_deflection
print(route_help_deflection())
PY
