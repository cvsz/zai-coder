#!/usr/bin/env bash
set -euo pipefail

APPLY="${APPLY:-0}"
SERVICE_NAME="${SERVICE_NAME:-zai-coder-control-plane}"
UNIT_PATH="/etc/systemd/system/${SERVICE_NAME}.service"

python3 - <<'PY'
from pathlib import Path
from zai_coder.deploy_installer_core.systemd import render_systemd_unit
Path("deploy/templates/zai-coder-control-plane.service").write_text(render_systemd_unit(), encoding="utf-8")
print("deploy/templates/zai-coder-control-plane.service")
PY

echo "target=$UNIT_PATH apply=$APPLY"
if [ "$APPLY" != "1" ]; then
  echo "DRY-RUN: set APPLY=1 to install systemd unit."
  exit 0
fi

sudo cp deploy/templates/zai-coder-control-plane.service "$UNIT_PATH"
sudo systemctl daemon-reload
sudo systemctl enable "$SERVICE_NAME.service"
sudo systemctl start "$SERVICE_NAME.service"
sudo systemctl status "$SERVICE_NAME.service" --no-pager
