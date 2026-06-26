#!/usr/bin/env bash
set -euo pipefail
OUT="${OUT:-releases/drafts/GITHUB_RELEASE_DRAFT.json}"
mkdir -p "$(dirname "$OUT")"
python3 - <<PY
from pathlib import Path
import json
from zai_coder.release_automation_update_center.routes import route_github_release_draft, route_github_release_command_plan
payload = {"draft": route_github_release_draft(), "commands": route_github_release_command_plan()}
Path("${OUT}").write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
print("${OUT}")
PY
