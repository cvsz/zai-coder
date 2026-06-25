#!/usr/bin/env bash
set -euo pipefail
OUT="${OUT:-assets/self-healing/self-healing-dashboard.html}"
mkdir -p "$(dirname "$OUT")"
python3 - <<PY
from pathlib import Path
from zai_coder.self_healing_operations.routes import route_self_healing_page
Path("${OUT}").write_text(route_self_healing_page()["html"], encoding="utf-8")
print("${OUT}")
PY
