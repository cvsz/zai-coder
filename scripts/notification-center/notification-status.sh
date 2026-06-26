#!/usr/bin/env bash
set -euo pipefail
python3 - <<'PY'
from zai_coder.notification_communication_center.routes import route_notification_center_status
print(route_notification_center_status())
PY
