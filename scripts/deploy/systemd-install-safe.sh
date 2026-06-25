#!/usr/bin/env bash
set -euo pipefail

APPLY="${APPLY:-0}"
SERVICE_SRC="${SERVICE_SRC:-deploy/systemd/zai-coder.service}"
SERVICE_DST="${SERVICE_DST:-/etc/systemd/system/zai-coder.service}"

echo "== Systemd install plan =="
echo "source: $SERVICE_SRC"
echo "target: $SERVICE_DST"
echo "apply:  $APPLY"

if [ "$APPLY" != "1" ]; then
  echo "DRY-RUN: set APPLY=1 to install service."
  exit 0
fi

sudo cp "$SERVICE_SRC" "$SERVICE_DST"
sudo systemctl daemon-reload
sudo systemctl enable zai-coder.service
echo "DONE: service installed. Start manually with: sudo systemctl start zai-coder"
