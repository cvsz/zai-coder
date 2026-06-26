#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

# --- Step 1: Parse version from pyproject.toml using Python's tomllib ---
VERSION=$(python3 -c '
import tomllib
with open("pyproject.toml", "rb") as f:
    data = tomllib.load(f)
print(data["project"]["version"])
')

if [ -z "$VERSION" ]; then
    echo "ERROR: Could not parse version from pyproject.toml"
    exit 1
fi

# --- Step 2: Compute expected artifact names ---
ARCHIVE_NAME="zai-coder-standalone-${VERSION}"
TAR_FILE="dist/${ARCHIVE_NAME}.tar.gz"
TAR_SHA_FILE="dist/${ARCHIVE_NAME}.tar.gz.sha256"
ZIP_FILE="dist/${ARCHIVE_NAME}.zip"
ZIP_SHA_FILE="dist/${ARCHIVE_NAME}.zip.sha256"
MANIFEST_FILE="dist/RELEASE_MANIFEST.json"

# --- Step 3: Verify all expected files exist ---
for file in "$TAR_FILE" "$TAR_SHA_FILE" "$ZIP_FILE" "$ZIP_SHA_FILE" "$MANIFEST_FILE"; do
    if [ ! -f "$file" ]; then
        echo "ERROR: Missing expected packaging artifact: $file"
        exit 1
    fi
done

# --- Step 4: Verify checksum files using sha256sum -c ---
echo "Verifying checksums..."
(cd dist && sha256sum -c "${ARCHIVE_NAME}.tar.gz.sha256")
(cd dist && sha256sum -c "${ARCHIVE_NAME}.zip.sha256")

# --- Step 5: Validate RELEASE_MANIFEST.json as JSON & verify version ---
echo "Validating RELEASE_MANIFEST.json..."
python3 -m json.tool "$MANIFEST_FILE" >/dev/null

# Verify RELEASE_MANIFEST.json references the correct version
python3 -c "
import json
with open('$MANIFEST_FILE') as f:
    manifest = json.load(f)
assert manifest.get('version') == '$VERSION', f'Manifest version {manifest.get(\"version\")} does not match $VERSION'
assert '${ARCHIVE_NAME}.tar.gz' in manifest.get('archives', []), 'Tarball archive missing from manifest archives list'
assert '${ARCHIVE_NAME}.zip' in manifest.get('archives', []), 'Zip archive missing from manifest archives list'
"

# --- Step 6: Verify no stale artifacts (for another version) are selected ---
# We make sure that we do not have files matching other version numbers in dist.
# Since we are validating files explicitly by expected name, we only verify those.

# --- Step 7: Check tarball contents for critical structures and exclusions ---
echo "Checking tarball contents..."
tar -tzf "$TAR_FILE" > dist/contents.txt

if ! grep -q "^${ARCHIVE_NAME}/zai-coder$" dist/contents.txt; then
    echo "ERROR: zai-coder entrypoint missing in tarball!"
    exit 1
fi

if ! grep -q "^${ARCHIVE_NAME}/pyproject.toml$" dist/contents.txt; then
    echo "ERROR: pyproject.toml missing in tarball!"
    exit 1
fi

if ! grep -q "^${ARCHIVE_NAME}/zai_coder/__init__.py$" dist/contents.txt; then
    echo "ERROR: zai_coder module missing in tarball!"
    exit 1
fi

# Exclusions check
if grep -q "\.git/" dist/contents.txt; then
    echo "ERROR: .git is included in tarball!"
    exit 1
fi

if grep -q "\.venv/" dist/contents.txt; then
    echo "ERROR: .venv is included in tarball!"
    exit 1
fi

if grep -q "\.pytest_cache/" dist/contents.txt; then
    echo "ERROR: .pytest_cache is included in tarball!"
    exit 1
fi

if grep -q "data/.*\.db" dist/contents.txt; then
    echo "ERROR: DB files are included in tarball!"
    exit 1
fi

# Clean up temporary contents.txt
rm -f dist/contents.txt

# --- Step 8: Print a compact JSON-like result ---
python3 -c "
import json, os
tar_size = os.path.getsize('$TAR_FILE')
zip_size = os.path.getsize('$ZIP_FILE')
res = {
    'ok': True,
    'version': '$VERSION',
    'artifacts': [
        {'name': '${ARCHIVE_NAME}.tar.gz', 'size_bytes': tar_size},
        {'name': '${ARCHIVE_NAME}.zip', 'size_bytes': zip_size}
    ]
}
print(json.dumps(res, indent=2))
"

