#!/usr/bin/env bash
set -euo pipefail

PREFIX="${PREFIX:-${HOME}/.local/share/zai-coder}"
APPLY="${APPLY:-0}"
LAUNCHER="${LAUNCHER:-${HOME}/.local/bin/zai-coder}"

echo "== ZAI Coder Uninstall Plan =="
echo "PREFIX: ${PREFIX}"
echo "LAUNCHER: ${LAUNCHER}"
echo "APPLY:  ${APPLY}"

if [[ "${APPLY}" != "1" ]]; then
  echo "DRY-RUN: Run 'APPLY=1 make uninstall' to execute."
  exit 0
fi

rm -rf "${PREFIX}"
rm -f "${LAUNCHER}"

echo "Uninstallation complete."
