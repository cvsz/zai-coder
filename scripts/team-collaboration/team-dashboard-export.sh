#!/usr/bin/env bash
set -euo pipefail
OUT="${OUT:-assets/team-collaboration/team-collaboration-dashboard.html}"
mkdir -p "$(dirname "$OUT")"
printf '<h1>Team Collaboration and Workspaces</h1>\n' > "$OUT"
echo "$OUT"
