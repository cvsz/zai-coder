#!/usr/bin/env bash
set -euo pipefail
HOSTNAME="${HOSTNAME:-zai.example.com}"
python3 - <<PY
from zai_coder.cloudflare_go_live.hostname_validator import validate_hostname
print(validate_hostname("${HOSTNAME}"))
PY
