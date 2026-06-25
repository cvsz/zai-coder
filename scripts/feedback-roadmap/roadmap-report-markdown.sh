#!/usr/bin/env bash
set -euo pipefail
OUT="${OUT:-roadmap/reports/FEEDBACK_ROADMAP_PREVIEW.md}"
mkdir -p "$(dirname "$OUT")"
python3 - <<PY
from pathlib import Path
from zai_coder.feedback_roadmap_center.routes import route_roadmap_report_markdown
Path("${OUT}").write_text(route_roadmap_report_markdown()["markdown"], encoding="utf-8")
print("${OUT}")
PY
