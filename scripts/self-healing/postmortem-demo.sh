#!/usr/bin/env bash
set -euo pipefail
OUT="${OUT:-incidents/reports/POSTMORTEM_DEMO.md}"
mkdir -p "$(dirname "$OUT")"
python3 - <<PY
from pathlib import Path
from zai_coder.self_healing_operations.routes import route_postmortem_demo
Path("${OUT}").write_text(route_postmortem_demo()["markdown"], encoding="utf-8")
print("${OUT}")
PY
