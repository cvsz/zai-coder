#!/usr/bin/env bash
set -euo pipefail
REPO_NAME="${REPO_NAME:-zai-coder-control-plane}"
VISIBILITY="${VISIBILITY:-public}"
APPLY="${APPLY:-0}"
APPROVAL_ID="${APPROVAL_ID:-}"
python3 - <<PY
import os
from zai_coder.real_provider_adapters.routes import route_github_create_repo_plan
print(route_github_create_repo_plan({"repo_name":"${REPO_NAME}","visibility":"${VISIBILITY}","apply":"${APPLY}"=="1","approval_id":"${APPROVAL_ID}","env":dict(os.environ),"scopes":["providers:plan","providers:apply"]}))
PY
