#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

VERSION=$(python3 -c "import zai_coder; print(zai_coder.__version__)")
if [ -z "$VERSION" ]; then
    VERSION="0.0.0"
fi

ARCHIVE_NAME="zai-coder-standalone-${VERSION}"

if [ ! -f "dist/${ARCHIVE_NAME}.tar.gz" ]; then
    echo "Archive not found: dist/${ARCHIVE_NAME}.tar.gz"
    exit 1
fi

echo "Checking tarball contents..."

# List contents
tar -tzf "dist/${ARCHIVE_NAME}.tar.gz" > dist/contents.txt

# Check that critical files exist
if ! grep -q "^${ARCHIVE_NAME}/zai-coder$" dist/contents.txt; then
    echo "ERROR: zai-coder entrypoint missing!"
    exit 1
fi

if ! grep -q "^${ARCHIVE_NAME}/pyproject.toml$" dist/contents.txt; then
    echo "ERROR: pyproject.toml missing!"
    exit 1
fi

if ! grep -q "^${ARCHIVE_NAME}/zai_coder/__init__.py$" dist/contents.txt; then
    echo "ERROR: zai_coder module missing!"
    exit 1
fi

# Check exclusions
if grep -q "\.git/" dist/contents.txt; then
    echo "ERROR: .git is included!"
    exit 1
fi

if grep -q "\.venv/" dist/contents.txt; then
    echo "ERROR: .venv is included!"
    exit 1
fi

if grep -q "\.pytest_cache/" dist/contents.txt; then
    echo "ERROR: .pytest_cache is included!"
    exit 1
fi

if grep -q "data/.*\.db" dist/contents.txt; then
    echo "ERROR: DB files are included!"
    exit 1
fi

echo "Package check: OK"
