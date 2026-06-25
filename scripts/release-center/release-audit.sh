#!/usr/bin/env bash
set -euo pipefail
APPLY="${APPLY:-0}"
if [ "$APPLY" = "1" ]; then
  python3 - <<'PY'
from zai_coder.release_automation_update_center.routes import route_release_audit_demo
print(route_release_audit_demo())
PY
else
  python3 - <<'PY'
from zai_coder.release_automation_update_center.routes import route_release_audit
print(route_release_audit())
PY
fi
