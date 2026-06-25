#!/usr/bin/env bash
set -euo pipefail
HOSTNAME="${HOSTNAME:-zai.example.com}"
TUNNEL_NAME="${TUNNEL_NAME:-zai-coder-control-plane}"
APPLY="${APPLY:-0}"
APPROVAL_ID="${APPROVAL_ID:-}"
python3 - <<PY
import os
from zai_coder.real_provider_adapters.routes import route_cloudflare_tunnel_plan
print(route_cloudflare_tunnel_plan({"hostname":"${HOSTNAME}","tunnel_name":"${TUNNEL_NAME}","apply":"${APPLY}"=="1","approval_id":"${APPROVAL_ID}","env":dict(os.environ),"scopes":["providers:plan","providers:apply"]}))
PY
