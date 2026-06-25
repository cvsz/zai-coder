#!/usr/bin/env bash
set -euo pipefail
ADMIN_EMAIL="${ADMIN_EMAIL:-admin@example.com}"
ORG_SLUG="${ORG_SLUG:-default-org}"
WORKSPACE_SLUG="${WORKSPACE_SLUG:-default}"
python3 - <<PY
from zai_coder.production_saas_core.wizards.first_run import build_first_run_plan
print(build_first_run_plan("${ADMIN_EMAIL}", "${ORG_SLUG}", "${WORKSPACE_SLUG}").to_dict())
PY
