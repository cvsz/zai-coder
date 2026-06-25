#!/usr/bin/env bash
set -euo pipefail
HOSTNAME="${HOSTNAME:-zai.example.com}"
MODE="${MODE:-local-cloudflare}"
python3 - <<PY
from zai_coder.production_saas_core.wizards.deployment import build_deployment_plan
print(build_deployment_plan("${HOSTNAME}", "${MODE}").to_dict())
PY
