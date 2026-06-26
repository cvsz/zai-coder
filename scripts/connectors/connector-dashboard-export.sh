#!/usr/bin/env bash
set -euo pipefail
OUT="${OUT:-assets/connectors/connector-dashboard.html}"
mkdir -p "$(dirname "$OUT")"
python3 - <<PY
from pathlib import Path
from zai_coder.plugin_connector_hub.routes import route_connector_page
Path("${OUT}").write_text(route_connector_page()["html"], encoding="utf-8")
print("${OUT}")
PY
