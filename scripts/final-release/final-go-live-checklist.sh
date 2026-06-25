#!/usr/bin/env bash
set -euo pipefail
python3 - <<'PY'
from zai_coder.final_enterprise_release_pack.routes import route_final_go_live_checklist
print(route_final_go_live_checklist())
PY
