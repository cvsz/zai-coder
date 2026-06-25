#!/usr/bin/env bash
set -euo pipefail
python3 - <<'PY'
from zai_coder.enterprise_governance.routes import route_compliance_checklist
print(route_compliance_checklist())
PY
