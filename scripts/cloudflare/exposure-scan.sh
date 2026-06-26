#!/usr/bin/env bash
set -euo pipefail
python3 - <<'PY'
from zai_coder.cloudflare_go_live.exposure_scan import exposure_scan_plan
report = exposure_scan_plan(".")
print(report)
if not report["ok"]:
    raise SystemExit(1)
PY
