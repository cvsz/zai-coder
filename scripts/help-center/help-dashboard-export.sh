#!/usr/bin/env bash
set -euo pipefail
OUT="${OUT:-assets/help-center/help-center-dashboard.html}"
mkdir -p "$(dirname "$OUT")"
python3 - <<PY
from pathlib import Path
from zai_coder.knowledge_base_help_center.routes import route_help_page
Path("${OUT}").write_text(route_help_page()["html"], encoding="utf-8")
print("${OUT}")
PY
