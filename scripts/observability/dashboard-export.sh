#!/usr/bin/env bash
set -euo pipefail
OUT="${OUT:-assets/observability/observability-dashboard.html}"
mkdir -p "$(dirname "$OUT")"
python3 - <<PY
from pathlib import Path
from zai_coder.observability_suite.routes import route_observability_page
Path("${OUT}").write_text(route_observability_page()["html"], encoding="utf-8")
print("${OUT}")
PY
