#!/usr/bin/env bash
set -euo pipefail
python3 - <<'PY'
from zai_coder.developer_portal_api_docs.routes import route_sdk_snippets
print(route_sdk_snippets())
PY
