#!/usr/bin/env bash
set -euo pipefail
APPLY="${APPLY:-0}"
if [ "$APPLY" != "1" ]; then
  python3 - <<'PY'
from zai_coder.enterprise_compliance_center.routes import route_audit_package_plan
print(route_audit_package_plan())
PY
  exit 0
fi
python3 - <<'PY'
from zai_coder.enterprise_compliance_center.routes import route_audit_readiness_demo
print(route_audit_readiness_demo())
PY
