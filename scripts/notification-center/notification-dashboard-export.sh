#!/usr/bin/env bash
set -euo pipefail
OUT="${OUT:-assets/notification-center/notification-center-dashboard.html}"
mkdir -p "$(dirname "$OUT")"
python3 - <<PY
from pathlib import Path
from zai_coder.notification_communication_center.routes import route_notifications_page
Path("${OUT}").write_text(route_notifications_page()["html"], encoding="utf-8")
print("${OUT}")
PY
