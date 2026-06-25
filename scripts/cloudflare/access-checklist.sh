#!/usr/bin/env bash
set -euo pipefail
HOSTNAME="${HOSTNAME:-zai.example.com}"
python3 - <<PY
from zai_coder.cloudflare_go_live.models import CloudflareGoLiveConfig
from zai_coder.cloudflare_go_live.access_policy import access_policy_checklist
for item in access_policy_checklist(CloudflareGoLiveConfig(hostname="${HOSTNAME}")):
    print(f"[{'REQUIRED' if item['required'] else 'OPTIONAL'}] {item['area']}: {item['item']}")
PY
