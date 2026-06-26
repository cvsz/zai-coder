#!/usr/bin/env bash
set -euo pipefail
python3 - <<'PY'
from zai_coder.production_saas_core.routes import route_saas_status, route_billing_dashboard, route_usage_dashboard, route_audit_dashboard
print(route_saas_status())
print(route_billing_dashboard()["html"][:300])
print(route_usage_dashboard([{"resource":"agent_run","units":1,"source":"demo"}], [{"resource":"agent_run","used":1,"limit":50,"allowed":True}])["html"][:300])
print(route_audit_dashboard([{"actor":"system","action":"demo","target":"audit","created_at":"now"}])["html"][:300])
PY
