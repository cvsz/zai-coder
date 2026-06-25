#!/usr/bin/env bash
set -euo pipefail
OUT="${OUT:-assets/execution/execution-timeline.html}"
mkdir -p "$(dirname "$OUT")"
python3 - <<PY
from pathlib import Path
from zai_coder.execution_runner.routes import route_execution_timeline
Path("${OUT}").write_text(route_execution_timeline()["html"], encoding="utf-8")
print("${OUT}")
PY
