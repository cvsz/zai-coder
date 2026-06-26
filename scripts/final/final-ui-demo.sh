#!/usr/bin/env bash
set -euo pipefail
python3 - <<'PY'
from zai_coder.app_studio_final.routes import route_home, route_plugins, route_workflows, route_models, route_deployments
print(route_home()["html"][:300])
print(route_plugins()["html"][:300])
print(route_workflows()["html"][:300])
print(route_models()["html"][:300])
print(route_deployments()["html"][:300])
PY
