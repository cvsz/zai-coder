#!/usr/bin/env bash
set -euo pipefail
APPLY="${APPLY:-0}"
if [ "$APPLY" != "1" ]; then
  echo "DRY-RUN: set APPLY=1 to write notification export/report files."
  exit 0
fi
python3 - <<'PY'
from zai_coder.notification_communication_center.routes import route_notification_export
print(route_notification_export())
PY
