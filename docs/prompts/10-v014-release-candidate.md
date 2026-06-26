# Prompt: v0.1.4 Release Candidate

```text
You are working locally in:

/home/zeazdev/zai-coder

Phase:
v0.1.4 Release Candidate — Version Bump and Local Artifact Validation

Branch:
release/v0.1.4

Goal:
Prepare the v0.1.4 release candidate after final readiness is merged. This is the first phase where the package version may be bumped to 0.1.4. Do not create tag, GitHub release, or upload assets before the release candidate PR is merged.

Critical rules:
- Version bump to 0.1.4 is allowed only in this phase.
- Do not create v0.1.4 tag.
- Do not publish GitHub release.
- Do not upload release assets.
- No direct main commit.
- Do not commit dist artifacts.
- Stage exact files only.

Steps:

cd /home/zeazdev/zai-coder

git fetch origin --prune --tags
git switch main
git pull --ff-only origin main
git status --short
git switch -c release/v0.1.4

Verify pre-bump version:

python3 - <<'PY'
import tomllib
from pathlib import Path

data = tomllib.loads(Path('pyproject.toml').read_text())
print(data['project']['version'])
PY

Bump version:
- pyproject.toml: 0.1.4
- zai_coder/__init__.py: __version__ = '0.1.4'

Create/update:
- docs/release/RELEASE_NOTES_v0.1.4.md
- docs/release/V0.1.4_RELEASE_CANDIDATE.md
- docs/release/V0.1.4_TASK_CHECKLIST.md

Validation:

python3 -m compileall -q zai_coder
python3 -m pytest -q
make repo-check
make secret-scan
make stage-manifest-check
./scripts/repo/check-generated-state.sh
./scripts/repo/check-ci-pytest-setup.sh
make package APPLY=1
make package-check

Verify no tag/release:

git tag --list 'v0.1.4'
gh release view v0.1.4 --repo cvsz/zai-coder >/tmp/zai-v014-release-view.txt 2>&1 || true
sed -n '1,120p' /tmp/zai-v014-release-view.txt

Expected artifacts are local only:
- dist/zai-coder-standalone-0.1.4.tar.gz
- dist/zai-coder-standalone-0.1.4.tar.gz.sha256
- dist/zai-coder-standalone-0.1.4.zip
- dist/zai-coder-standalone-0.1.4.zip.sha256
- dist/RELEASE_MANIFEST.json

Do not commit dist.

Stage exact files:

git add pyproject.toml
git add zai_coder/__init__.py
git add docs/release/RELEASE_NOTES_v0.1.4.md
git add docs/release/V0.1.4_RELEASE_CANDIDATE.md
git add docs/release/V0.1.4_TASK_CHECKLIST.md

git commit -S -m "release: prepare v0.1.4 candidate"
git push -u origin release/v0.1.4

gh pr create \
  --base main \
  --head release/v0.1.4 \
  --draft \
  --title "release: prepare v0.1.4 candidate" \
  --body-file docs/release/V0.1.4_RELEASE_CANDIDATE.md

Report:
1. branch
2. main baseline
3. version before/after
4. validation result
5. package-check result
6. no tag/release/upload verification
7. generated-file exclusion
8. commit hash
9. draft PR URL
```
