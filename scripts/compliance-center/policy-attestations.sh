#!/usr/bin/env bash
set -euo pipefail
python3 - <<'PY'
from zai_coder.enterprise_compliance_center.routes import route_policy_attestations
print(route_policy_attestations())
PY
