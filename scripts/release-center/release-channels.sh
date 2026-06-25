#!/usr/bin/env bash
set -euo pipefail
CHANNEL="${CHANNEL:-stable}"
python3 - <<PY
from zai_coder.release_automation_update_center.routes import route_release_channels, route_release_channel_policy
print(route_release_channels())
print(route_release_channel_policy("${CHANNEL}"))
PY
