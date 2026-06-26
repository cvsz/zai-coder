#!/usr/bin/env bash
set -euo pipefail
python3 - <<'PY'
from zai_coder.security_operations_threat_monitoring.routes import route_incident_workflow_plan
print(route_incident_workflow_plan())
PY
