#!/usr/bin/env bash
set -euo pipefail
python3 - <<'PY'
from zai_coder.usage_analytics_insights.routes import route_usage_analytics_status
print(route_usage_analytics_status())
PY
