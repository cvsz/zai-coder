#!/usr/bin/env bash
set -euo pipefail
python3 - <<'PY'
from zai_coder.enterprise_reporting_board_pack.routes import route_narrative_bundle
print(route_narrative_bundle())
PY
