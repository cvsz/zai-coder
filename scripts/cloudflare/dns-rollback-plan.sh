#!/usr/bin/env bash
set -euo pipefail
HOSTNAME="${HOSTNAME:-zai.example.com}"
python3 - <<PY
from zai_coder.cloudflare_go_live.models import CloudflareGoLiveConfig
from zai_coder.cloudflare_go_live.dns_planner import dns_rollback_plan
print(dns_rollback_plan(CloudflareGoLiveConfig(hostname="${HOSTNAME}")).to_dict())
PY
