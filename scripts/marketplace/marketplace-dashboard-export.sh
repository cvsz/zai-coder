#!/usr/bin/env bash
set -euo pipefail
OUT="${OUT:-assets/marketplace/marketplace-dashboard.html}"
mkdir -p "$(dirname "$OUT")"
python3 - <<PY
from pathlib import Path
from zai_coder.agent_marketplace_and_skills.routes import route_marketplace_page
Path("${OUT}").write_text(route_marketplace_page()["html"], encoding="utf-8")
print("${OUT}")
PY
