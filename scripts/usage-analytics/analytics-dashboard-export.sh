#!/usr/bin/env bash
set -euo pipefail
OUT="${OUT:-assets/usage-analytics/usage-analytics-dashboard.html}"
mkdir -p "$(dirname "$OUT")"
python3 - <<PY
from pathlib import Path
from zai_coder.usage_analytics_insights.routes import route_analytics_page
Path("${OUT}").write_text(route_analytics_page()["html"], encoding="utf-8")
print("${OUT}")
PY
