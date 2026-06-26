#!/usr/bin/env bash
set -euo pipefail
OUT="${OUT:-assets/payments/payment-dashboard.html}"
mkdir -p "$(dirname "$OUT")"
python3 - <<PY
from pathlib import Path
from zai_coder.payment_provider_sandbox.routes import route_payment_page
Path("${OUT}").write_text(route_payment_page()["html"], encoding="utf-8")
print("${OUT}")
PY
