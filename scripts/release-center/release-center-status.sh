#!/usr/bin/env bash
set -euo pipefail
python3 - <<'PY'
from zai_coder.release_automation_update_center.routes import route_release_center_status
print(route_release_center_status())
PY
