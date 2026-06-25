#!/usr/bin/env bash
set -euo pipefail
APPLY="${APPLY:-0}"
if [ "$APPLY" != "1" ]; then
  python3 - <<'PY'
from zai_coder.agent_marketplace_and_skills.routes import route_skill_pack_plan
print(route_skill_pack_plan())
PY
  exit 0
fi
python3 - <<'PY'
from zai_coder.agent_marketplace_and_skills.routes import route_skill_pack_build
print(route_skill_pack_build())
PY
