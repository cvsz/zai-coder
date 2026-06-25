#!/usr/bin/env bash
set -euo pipefail
OUT="${OUT:-assets/ops-center/health-dashboard.html}"
mkdir -p "$(dirname "$OUT")"
python3 - <<PY
from pathlib import Path
from zai_coder.operations_control_center.health_dashboard import render_health_dashboard
Path("${OUT}").write_text(render_health_dashboard(), encoding="utf-8")
print("${OUT}")
PY
