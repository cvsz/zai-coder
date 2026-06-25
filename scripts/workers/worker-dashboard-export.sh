#!/usr/bin/env bash
set -euo pipefail
OUT="${OUT:-assets/workers/worker-dashboard.html}"
mkdir -p "$(dirname "$OUT")"
python3 - <<PY
from pathlib import Path
from zai_coder.worker_orchestration.routes import route_worker_page
Path("${OUT}").write_text(route_worker_page()["html"], encoding="utf-8")
print("${OUT}")
PY
