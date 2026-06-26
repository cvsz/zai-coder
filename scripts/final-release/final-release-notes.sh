#!/usr/bin/env bash
set -euo pipefail
python3 - <<'PY'
from zai_coder.final_enterprise_release_pack.routes import route_final_release_notes
print(route_final_release_notes())
PY
