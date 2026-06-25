#!/usr/bin/env bash
set -euo pipefail
OUT="${OUT:-analytics/reports/USAGE_ANALYTICS_PREVIEW.md}"
mkdir -p "$(dirname "$OUT")"
python3 - <<PY
from pathlib import Path
from zai_coder.usage_analytics_insights.routes import route_analytics_report_markdown
Path("${OUT}").write_text(route_analytics_report_markdown()["markdown"], encoding="utf-8")
print("${OUT}")
PY
