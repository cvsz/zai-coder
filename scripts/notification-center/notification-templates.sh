#!/usr/bin/env bash
set -euo pipefail
python3 - <<'PY'
from zai_coder.notification_communication_center.routes import route_notification_templates
print(route_notification_templates())
PY
