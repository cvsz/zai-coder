#!/usr/bin/env bash
set -euo pipefail
OUT="${OUT:-assets/compliance-center/compliance-dashboard.html}"
mkdir -p "$(dirname "$OUT")"
python3 - <<PY
from pathlib import Path
from zai_coder.enterprise_compliance_center.routes import route_compliance_page
Path("${OUT}").write_text(route_compliance_page()["html"], encoding="utf-8")
print("${OUT}")
PY
