#!/usr/bin/env bash
set -euo pipefail
OUT="${OUT:-assets/governance/governance-dashboard.html}"
mkdir -p "$(dirname "$OUT")"
python3 - <<PY
from pathlib import Path
from zai_coder.enterprise_governance.routes import route_governance_page
Path("${OUT}").write_text(route_governance_page()["html"], encoding="utf-8")
print("${OUT}")
PY
