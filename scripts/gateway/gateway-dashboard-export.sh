#!/usr/bin/env bash
set -euo pipefail
OUT="${OUT:-assets/gateway/gateway-dashboard.html}"
mkdir -p "$(dirname "$OUT")"
python3 - <<PY
from pathlib import Path
from zai_coder.production_api_gateway.routes import route_gateway_page
Path("${OUT}").write_text(route_gateway_page()["html"], encoding="utf-8")
print("${OUT}")
PY
