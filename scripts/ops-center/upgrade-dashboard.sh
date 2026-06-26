#!/usr/bin/env bash
set -euo pipefail
VERSION="${VERSION:-v0.15.0}"
OUT="${OUT:-assets/ops-center/upgrade-dashboard.html}"
mkdir -p "$(dirname "$OUT")"
python3 - <<PY
from pathlib import Path
from zai_coder.operations_control_center.upgrade_dashboard import render_upgrade_dashboard
Path("${OUT}").write_text(render_upgrade_dashboard("${VERSION}"), encoding="utf-8")
print("${OUT}")
PY
