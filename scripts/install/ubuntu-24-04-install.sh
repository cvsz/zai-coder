#!/usr/bin/env bash
set -euo pipefail

APPLY="${APPLY:-0}"
echo "== Ubuntu 24.04 install plan =="
echo "Packages: python3 python3-venv python3-pip curl ca-certificates"
if [ "$APPLY" != "1" ]; then
  echo "DRY-RUN: set APPLY=1 to install packages."
  exit 0
fi

sudo apt-get update
sudo apt-get install -y python3 python3-venv python3-pip curl ca-certificates
./install.sh APPLY=1
