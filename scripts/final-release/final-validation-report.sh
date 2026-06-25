#!/usr/bin/env bash
set -euo pipefail
python3 - <<'PY'
from zai_coder.final_enterprise_release_pack.routes import route_final_validation_report
print(route_final_validation_report())
PY
