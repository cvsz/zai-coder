# Prompt: v0.1.4 Publish

```text
You are working locally in:

/home/zeazdev/zai-coder

Phase:
v0.1.4 Publish — Signed Tag, GitHub Release, Asset Upload, and Verification

Goal:
Publish v0.1.4 only after the release candidate PR has merged into main and main is verified at version 0.1.4. This is the phase where signed tag creation, GitHub release creation, and asset upload are allowed.

Critical rules:
- Create v0.1.4 tag only after main is verified.
- Do not rewrite existing tags.
- Do not replace release assets without recovery plan.
- No direct main source changes.
- Do not commit dist artifacts.
- Stage exact verification docs only if needed.

Steps:

cd /home/zeazdev/zai-coder

git fetch origin --prune --tags
git switch main
git pull --ff-only origin main
git status --short

Verify version:

python3 - <<'PY'
import tomllib
from pathlib import Path

data = tomllib.loads(Path('pyproject.toml').read_text())
assert data['project']['version'] == '0.1.4'
print(data['project']['version'])
PY

python3 - <<'PY'
import zai_coder
assert getattr(zai_coder, '__version__', None) == '0.1.4'
print(zai_coder.__version__)
PY

Verify no existing v0.1.4 tag/release:

git tag --list 'v0.1.4'
gh release view v0.1.4 --repo cvsz/zai-coder >/tmp/zai-v014-release-view-before.txt 2>&1 || true
sed -n '1,160p' /tmp/zai-v014-release-view-before.txt

Validation and package:

python3 -m compileall -q zai_coder
python3 -m pytest -q
make repo-check
make secret-scan
make stage-manifest-check
./scripts/repo/check-generated-state.sh
./scripts/repo/check-ci-pytest-setup.sh
make package APPLY=1
make package-check

Verify checksums:

sha256sum -c dist/zai-coder-standalone-0.1.4.tar.gz.sha256
sha256sum -c dist/zai-coder-standalone-0.1.4.zip.sha256

Create signed tag:

git tag -s v0.1.4 -m "ZAI Coder v0.1.4"
git tag -v v0.1.4
git push origin v0.1.4

Create GitHub release:

gh release create v0.1.4 \
  --repo cvsz/zai-coder \
  --title "v0.1.4" \
  --notes-file docs/release/RELEASE_NOTES_v0.1.4.md \
  dist/RELEASE_MANIFEST.json \
  dist/zai-coder-standalone-0.1.4.tar.gz \
  dist/zai-coder-standalone-0.1.4.tar.gz.sha256 \
  dist/zai-coder-standalone-0.1.4.zip \
  dist/zai-coder-standalone-0.1.4.zip.sha256

Verify release:

gh release view v0.1.4 --repo cvsz/zai-coder --json tagName,name,isDraft,isPrerelease,url,assets,targetCommitish

Report:
1. main HEAD
2. version verified
3. validation result
4. package-check result
5. tag SHA
6. tag verification
7. GitHub release URL
8. uploaded assets
9. generated-file exclusion
10. next post-release verification branch
```
