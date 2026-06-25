#!/usr/bin/env bash
set -euo pipefail
python3 - <<'PY'
from zai_coder.usage_analytics_insights.routes import route_analytics_funnel
print(route_analytics_funnel())
PY
