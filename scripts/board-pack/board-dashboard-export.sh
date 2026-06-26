#!/usr/bin/env bash
set -euo pipefail
OUT="${OUT:-assets/board-pack/board-pack-dashboard.html}"
mkdir -p "$(dirname "$OUT")"
python3 - <<PY
from pathlib import Path
from zai_coder.enterprise_reporting_board_pack.routes import route_board_pack_page
Path("${OUT}").write_text(route_board_pack_page()["html"], encoding="utf-8")
print("${OUT}")
PY
