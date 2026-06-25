#!/usr/bin/env bash
set -euo pipefail
OUT="${OUT:-assets/content-studio/template-content-studio-dashboard.html}"
mkdir -p "$(dirname "$OUT")"
python3 - <<PY
from pathlib import Path
from zai_coder.template_content_studio.routes import route_content_studio_page
Path("${OUT}").write_text(route_content_studio_page()["html"], encoding="utf-8")
print("${OUT}")
PY
