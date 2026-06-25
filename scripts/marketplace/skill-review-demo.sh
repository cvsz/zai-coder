#!/usr/bin/env bash
set -euo pipefail
APPLY="${APPLY:-0}"
if [ "$APPLY" != "1" ]; then
  echo "DRY-RUN: set APPLY=1 to create demo skill review."
  exit 0
fi
python3 - <<'PY'
from zai_coder.agent_marketplace_and_skills.routes import route_skill_review_demo
print(route_skill_review_demo())
PY
