#!/usr/bin/env bash
set -euo pipefail
APPLY="${APPLY:-0}"
NAME="${NAME:-zai-coder-control-plane}"
python3 - <<PY
from zai_coder.deployment_core.release_builder import build_release_zip
print(build_release_zip(".", "release", "${NAME}", apply="${APPLY}"=="1").to_dict())
PY
