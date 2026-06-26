#!/usr/bin/env bash
set -euo pipefail
TITLE="${TITLE:-Service degradation}"
SEVERITY="${SEVERITY:-sev3}"
OUT="${OUT:-assets/observability/incident-template.md}"
mkdir -p "$(dirname "$OUT")"
python3 - <<PY
from pathlib import Path
from zai_coder.observability_suite.routes import route_incident_template
payload = route_incident_template("${TITLE}", "${SEVERITY}")
Path("${OUT}").write_text(payload["markdown"], encoding="utf-8")
print("${OUT}")
PY
