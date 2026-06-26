#!/usr/bin/env bash
set -euo pipefail
python3 - <<'PY'
from zai_coder.enterprise_sso_identity_center.routes import route_scim_mapping_draft
print(route_scim_mapping_draft())
PY
