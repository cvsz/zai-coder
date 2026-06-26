#!/usr/bin/env bash
set -euo pipefail
python3 - <<'PY'
from zai_coder.app_studio_final.routes import route_final_status
print(route_final_status())
PY
