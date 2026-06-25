#!/usr/bin/env bash
set -euo pipefail
OUT="${OUT:-assets/ops-center/backup-dashboard.html}"
mkdir -p "$(dirname "$OUT")"
python3 - <<PY
from pathlib import Path
from zai_coder.operations_control_center.backup_dashboard import render_backup_dashboard
Path("${OUT}").write_text(render_backup_dashboard(), encoding="utf-8")
print("${OUT}")
PY
