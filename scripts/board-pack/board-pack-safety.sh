#!/usr/bin/env bash
set -euo pipefail
python3 - <<'PY'
from zai_coder.enterprise_reporting_board_pack.routes import route_board_pack_safety
print(route_board_pack_safety())
PY
