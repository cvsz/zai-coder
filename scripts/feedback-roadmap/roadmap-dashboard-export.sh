#!/usr/bin/env bash
set -euo pipefail
OUT="${OUT:-assets/feedback-roadmap/feedback-roadmap-dashboard.html}"
mkdir -p "$(dirname "$OUT")"
python3 - <<PY
from pathlib import Path
from zai_coder.feedback_roadmap_center.routes import route_roadmap_page
Path("${OUT}").write_text(route_roadmap_page()["html"], encoding="utf-8")
print("${OUT}")
PY
