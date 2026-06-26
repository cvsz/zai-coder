#!/usr/bin/env bash
set -euo pipefail
PROVIDER="${PROVIDER:-github}"
APPLY="${APPLY:-0}"
python3 - <<PY
import os
from zai_coder.real_provider_adapters.env_validation import validate_provider_env
print(validate_provider_env("${PROVIDER}", dict(os.environ), apply="${APPLY}"=="1"))
PY
