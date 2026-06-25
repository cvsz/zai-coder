#!/usr/bin/env bash
set -euo pipefail
OUT="${OUT:-assets/billing/billing-dashboard.html}"
mkdir -p "$(dirname "$OUT")"
python3 - <<PY
from pathlib import Path
from zai_coder.billing_usage_enforcement.routes import route_billing_page
Path("${OUT}").write_text(route_billing_page()["html"], encoding="utf-8")
print("${OUT}")
PY
