#!/usr/bin/env bash
set -euo pipefail
HOSTNAME="${HOSTNAME:-zai.example.com}"
TUNNEL_NAME="${TUNNEL_NAME:-zai-coder-control-plane}"
python3 - <<PY
from zai_coder.cloudflare_go_live.models import CloudflareGoLiveConfig
from zai_coder.cloudflare_go_live.go_live_wizard import go_live_wizard_plan
print(go_live_wizard_plan(CloudflareGoLiveConfig(hostname="${HOSTNAME}", tunnel_name="${TUNNEL_NAME}")).to_dict())
PY
