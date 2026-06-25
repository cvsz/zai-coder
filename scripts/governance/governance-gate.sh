#!/usr/bin/env bash
set -euo pipefail
python3 - <<'PY'
from zai_coder.enterprise_governance.routes import route_governance_gate
print(route_governance_gate({"mutating": True, "apply": False, "secret_scan_ok": True}))
PY
