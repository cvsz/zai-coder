#!/usr/bin/env bash
set -euo pipefail
DOMAIN="${DOMAIN:-zai.example.com}"
python3 - <<PY
from zai_coder.deploy_installer_core.config import DeployInstallConfig
from zai_coder.deploy_installer_core.cloudflare import cloudflare_plan
plan = cloudflare_plan(DeployInstallConfig(domain="${DOMAIN}"))
print(plan)
PY
