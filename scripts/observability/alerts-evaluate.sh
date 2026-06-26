#!/usr/bin/env bash
set -euo pipefail
python3 - <<'PY'
from zai_coder.observability_suite.routes import route_alert_rules, route_alerts_evaluate
print(route_alert_rules())
print(route_alerts_evaluate())
PY
