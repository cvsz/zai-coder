#!/usr/bin/env bash
set -euo pipefail
python3 - <<'PY'
from zai_coder.integration_core.adapters.cloudflare_adapter import CloudflareDnsRecord, dns_plan, tunnel_validate_plan
print(tunnel_validate_plan().to_dict())
print(dns_plan([CloudflareDnsRecord("zai.zeaz.dev", "CNAME", "tunnel.example.com")]).to_dict())
PY
