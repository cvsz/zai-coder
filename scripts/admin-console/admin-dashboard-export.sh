#!/usr/bin/env bash
set -euo pipefail
OUT="${OUT:-assets/admin-console/admin-dashboard.html}"
mkdir -p "$(dirname "$OUT")"
python3 - <<PY
from pathlib import Path
from zai_coder.enterprise_admin_console.routes import route_admin_page
Path("${OUT}").write_text(route_admin_page()["html"], encoding="utf-8")
print("${OUT}")
PY
