#!/usr/bin/env bash
set -euo pipefail
python3 - <<'PY'
from zai_coder.enterprise_governance.routes import route_evidence_collect, route_evidence_bundle
print(route_evidence_collect("."))
print(route_evidence_bundle("."))
PY
