#!/usr/bin/env bash
set -euo pipefail
OUT="${OUT:-assets/tenants/tenant-dashboard.html}"
mkdir -p "$(dirname "$OUT")"
python3 - <<PY
from pathlib import Path
from zai_coder.multi_tenant_control.routes import route_tenant_page
Path("${OUT}").write_text(route_tenant_page()["html"], encoding="utf-8")
print("${OUT}")
PY
