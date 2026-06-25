#!/usr/bin/env bash
set -euo pipefail
python3 - <<'PY'
from zai_coder.enterprise_reporting_board_pack.routes import route_kpi_snapshot
print(route_kpi_snapshot())
PY
