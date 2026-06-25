#!/usr/bin/env bash
set -euo pipefail
TUNNEL_NAME="${TUNNEL_NAME:-zai-coder}"
HOSTNAME="${HOSTNAME:-zai.example.com}"
python3 - <<PY
from zai_coder.deployment_core.cloudflare_config import CloudflareTunnelConfig
print(CloudflareTunnelConfig("${TUNNEL_NAME}", "${HOSTNAME}").render_yaml())
PY
