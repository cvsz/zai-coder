#!/usr/bin/env bash
set -euo pipefail
OUT="${OUT:-releases/drafts/CHANGELOG_V29.md}"
mkdir -p "$(dirname "$OUT")"
python3 - <<PY
from pathlib import Path
from zai_coder.release_automation_update_center.routes import route_changelog_demo
Path("${OUT}").write_text(route_changelog_demo()["markdown"], encoding="utf-8")
print("${OUT}")
PY
