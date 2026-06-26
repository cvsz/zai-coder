#!/usr/bin/env bash
set -euo pipefail

VERSION="${VERSION:-${1:-v0.1.0}}"
MESSAGE="${MESSAGE:-${VERSION}}"
APPLY="${APPLY:-0}"

echo "== GPG signed tag plan =="
echo "version: $VERSION"
echo "message: $MESSAGE"
echo "apply:   $APPLY"

if [ "$APPLY" != "1" ]; then
  echo "DRY-RUN: set APPLY=1 to create signed tag."
  exit 0
fi

export GPG_TTY="${GPG_TTY:-$(tty)}"
git tag -s "$VERSION" -m "$MESSAGE"
git tag -v "$VERSION"
