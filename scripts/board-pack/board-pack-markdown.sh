#!/usr/bin/env bash
set -euo pipefail
OUT="${OUT:-reports/board-pack/BOARD_PACK_PREVIEW.md}"
mkdir -p "$(dirname "$OUT")"
python3 - <<PY
from pathlib import Path
from zai_coder.enterprise_reporting_board_pack.routes import route_board_pack_markdown
Path("${OUT}").write_text(route_board_pack_markdown()["markdown"], encoding="utf-8")
print("${OUT}")
PY
