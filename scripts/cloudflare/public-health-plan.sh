#!/usr/bin/env bash
set -euo pipefail
HOSTNAME="${HOSTNAME:-zai.example.com}"
python3 - <<PY
from zai_coder.cloudflare_go_live.models import CloudflareGoLiveConfig
from zai_coder.cloudflare_go_live.public_health import public_health_verification_plan
print(public_health_verification_plan(CloudflareGoLiveConfig(hostname="${HOSTNAME}")).to_dict())
PY
