#!/usr/bin/env bash
set -euo pipefail
APPLY="${APPLY:-0}"
MANIFEST="${MANIFEST:-docs/github/STAGE_MANIFEST.v12-github-ready.txt}"
# Safety marker: apps/zlms/**, node_modules/**, dist/**, .next/**, coverage/**, reports/**, .env* are blocked by stage manifest validation.
# Safety marker: apps/zlms/** is blocked by stage manifest validation.
python3 - <<PY
from zai_coder.github_ready_core.stage_manifest import load_stage_manifest, render_git_add_commands
for cmd in render_git_add_commands(load_stage_manifest("${MANIFEST}")):
    print(cmd)
PY
if [ "$APPLY" != "1" ]; then
  echo "DRY-RUN: set APPLY=1 to stage exact files."
  exit 0
fi
while IFS= read -r path; do
  [ -z "$path" ] && continue
  case "$path" in \#*) continue ;; esac
  git add -- "$path"
done < "$MANIFEST"
git status --short
