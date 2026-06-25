#!/usr/bin/env bash
set -euo pipefail
APPLY="${APPLY:-0}"
VERSION="${VERSION:-v0.12.0}"
NOTES="${NOTES:-docs/release/RELEASE_NOTES_v0.12.0.md}"
echo "version=$VERSION notes=$NOTES apply=$APPLY"
if [ "$APPLY" != "1" ]; then
  echo "DRY-RUN: set APPLY=1 to create draft release."
  exit 0
fi
gh release create "$VERSION" --draft --title "ZAI Coder Control Plane $VERSION" --notes-file "$NOTES"
