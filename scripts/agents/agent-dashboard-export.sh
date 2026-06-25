#!/usr/bin/env bash
set -euo pipefail
OUT="${OUT:-assets/agents/agent-dashboard.html}"
mkdir -p "$(dirname "$OUT")"
python3 - <<PY
from pathlib import Path
from zai_coder.agent_runtime_supervisor.routes import route_agent_page
Path("${OUT}").write_text(route_agent_page()["html"], encoding="utf-8")
print("${OUT}")
PY
