#!/usr/bin/env bash
set -euo pipefail
APPLY="${APPLY:-0}"
if [ "$APPLY" != "1" ]; then
  echo "DRY-RUN: set APPLY=1 to write board pack JSON/Markdown exports."
  exit 0
fi
python3 - <<'PY'
from zai_coder.enterprise_reporting_board_pack.routes import route_board_pack_demo
print(route_board_pack_demo())
PY
