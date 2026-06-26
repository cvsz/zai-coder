#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

VERSION=$(python3 -c "import zai_coder; print(zai_coder.__version__)")
if [ -z "$VERSION" ]; then
    VERSION="0.0.0"
fi

echo "Packaging version: $VERSION"

mkdir -p dist

ARCHIVE_NAME="zai-coder-standalone-${VERSION}"

# Create a temporary staging area to avoid packaging the current repo directly if we want a clean root folder inside the archive
TEMP_DIR=$(mktemp -d)
STAGING="$TEMP_DIR/$ARCHIVE_NAME"
mkdir -p "$STAGING"

# Copy everything except excluded
rsync -a --exclude '.git' \
    --exclude '.venv' \
    --exclude '__pycache__' \
    --exclude '*.pyc' \
    --exclude '.pytest_cache' \
    --exclude '.env' \
    --exclude 'data/*.db' \
    --exclude 'data/tasks.db' \
    --exclude 'data/migrations.db' \
    --exclude 'data/zai-audit.jsonl' \
    --exclude 'data/zai-memory.db' \
    --exclude 'dist' \
    --exclude 'reports' \
    --exclude 'out' \
    ./ "$STAGING/"

# Zip
cd "$TEMP_DIR"
zip -r "$ROOT/dist/${ARCHIVE_NAME}.zip" "$ARCHIVE_NAME" -q
tar -czf "$ROOT/dist/${ARCHIVE_NAME}.tar.gz" "$ARCHIVE_NAME"

cd "$ROOT/dist"
sha256sum "${ARCHIVE_NAME}.zip" > "${ARCHIVE_NAME}.zip.sha256"
sha256sum "${ARCHIVE_NAME}.tar.gz" > "${ARCHIVE_NAME}.tar.gz.sha256"

# Create RELEASE_MANIFEST.json
cat <<EOF > RELEASE_MANIFEST.json
{
  "version": "${VERSION}",
  "archives": [
    "${ARCHIVE_NAME}.zip",
    "${ARCHIVE_NAME}.tar.gz"
  ],
  "timestamp": "$(date -u +'%Y-%m-%dT%H:%M:%SZ')"
}
EOF

# Clean up
rm -rf "$TEMP_DIR"

echo "Packaging complete in dist/"
