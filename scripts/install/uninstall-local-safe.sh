#!/usr/bin/env bash
set -euo pipefail
PREFIX="${PREFIX:-${HOME}/.local/share/zai-coder}"
APPLY="${APPLY:-0}"

echo "== ZAI Coder Uninstall Plan =="
echo "PREFIX: $PREFIX"
echo "APPLY:  $APPLY"

if [ "$APPLY" != "1" ]; then
    echo "DRY-RUN: Run 'APPLY=1 make uninstall' to execute."
    exit 0
fi

rm -rf "$PREFIX"
rm -f "$HOME/.local/bin/zai-coder"

echo "Uninstallation complete."
EOF
