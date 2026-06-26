#!/usr/bin/env bash
set -euo pipefail
OUT="${OUT:-assets/observability/metrics.prom}"
mkdir -p "$(dirname "$OUT")"
python3 - <<PY
from pathlib import Path
from zai_coder.observability_suite.routes import route_metrics_prometheus
Path("${OUT}").write_text(route_metrics_prometheus()["text"], encoding="utf-8")
print("${OUT}")
PY
