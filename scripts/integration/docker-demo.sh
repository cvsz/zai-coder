#!/usr/bin/env bash
set -euo pipefail
python3 - <<'PY'
from zai_coder.integration_core.adapters.docker_adapter import docker_status_plan, safe_cleanup_plan
print(docker_status_plan().to_dict())
print(safe_cleanup_plan().to_dict())
PY
