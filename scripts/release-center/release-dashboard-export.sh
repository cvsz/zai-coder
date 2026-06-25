#!/usr/bin/env bash
set -euo pipefail
OUT="${OUT:-assets/release-center/release-center-dashboard.html}"
mkdir -p "$(dirname "$OUT")"
python3 - <<PY
from pathlib import Path
from zai_coder.release_automation_update_center.routes import route_release_center_page
Path("${OUT}").write_text(route_release_center_page()["html"], encoding="utf-8")
print("${OUT}")
PY
