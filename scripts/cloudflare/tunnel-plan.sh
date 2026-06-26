#!/usr/bin/env bash
set -euo pipefail
HOSTNAME="${HOSTNAME:-zai.example.com}"
TUNNEL_NAME="${TUNNEL_NAME:-zai-coder-control-plane}"
python3 - <<PY
from pathlib import Path
from zai_coder.cloudflare_go_live.models import CloudflareGoLiveConfig
from zai_coder.cloudflare_go_live.tunnel import tunnel_install_plan
cfg = CloudflareGoLiveConfig(hostname="${HOSTNAME}", tunnel_name="${TUNNEL_NAME}")
plan = tunnel_install_plan(cfg)
for path, content in plan.files.items():
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(content, encoding="utf-8")
print(plan.to_dict())
PY
