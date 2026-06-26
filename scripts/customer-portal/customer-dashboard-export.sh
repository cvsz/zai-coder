#!/usr/bin/env bash
set -euo pipefail
OUT="${OUT:-assets/customer-portal/customer-dashboard.html}"
mkdir -p "$(dirname "$OUT")"
python3 - <<PY
from pathlib import Path
from zai_coder.customer_portal_onboarding.routes import route_customer_page
Path("${OUT}").write_text(route_customer_page()["html"], encoding="utf-8")
print("${OUT}")
PY
