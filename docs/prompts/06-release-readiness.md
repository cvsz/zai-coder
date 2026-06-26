# Prompt: v0.1.4 Release Readiness Status

```text
You are working locally in:

/home/zeazdev/zai-coder

Phase:
v0.1.4 Implementation PR — Release Readiness Status and Preconditions

Branch:
chore/v0.1.4-release-readiness

Goal:
Add or improve a release readiness status command/script that verifies preconditions before release candidate and publish phases. This phase must not bump version, create tags, publish releases, or upload assets.

Critical rules:
- No version bump.
- No tag/release/asset mutation.
- No direct main commit.
- No generated runtime state committed.
- Stage exact files only.

Steps:

cd /home/zeazdev/zai-coder

git fetch origin --prune --tags
git switch main
git pull --ff-only origin main
git status --short
git switch -c chore/v0.1.4-release-readiness

Inspect release scripts:

find scripts docs tests -maxdepth 4 -type f | sort | grep -E 'release|package|manifest|status|guard|check' || true
grep -R "final-release-status\|package-check\|gh release\|git tag\|RELEASE_MANIFEST\|stage-manifest" -n scripts tests docs Makefile 2>/dev/null | head -420

Implement one focused improvement:
- create or improve scripts/final-release/release-readiness-status.sh; or
- add tests around existing final-release-status script; or
- add docs describing preconditions and outputs.

Readiness should check:
- clean git working tree
- version consistency
- required guard scripts exist
- generated-state guard passes
- CI pytest setup guard passes
- no unexpected dist tracking
- release docs/checklists present for the target phase

Recommended files:
- scripts/final-release/release-readiness-status.sh
- tests/test_release_readiness_v014.py
- docs/ops/release-readiness-status.md
- Makefile only if adding a target

Validation:

python3 -m pytest tests/test_release_readiness_v014.py -q
python3 -m pytest -q
python3 -m compileall -q zai_coder
make repo-check
make secret-scan
make stage-manifest-check
./scripts/repo/check-generated-state.sh
./scripts/repo/check-ci-pytest-setup.sh

git status --short

git add scripts/final-release/release-readiness-status.sh
git add tests/test_release_readiness_v014.py
git add docs/ops/release-readiness-status.md
# add Makefile exact path only if changed

git commit -S -m "chore: add release readiness status"
git push -u origin chore/v0.1.4-release-readiness

gh pr create \
  --base main \
  --head chore/v0.1.4-release-readiness \
  --draft \
  --title "chore: add release readiness status" \
  --body "Adds v0.1.4 release readiness precondition checks without mutating release state."

Report:
1. branch
2. readiness checks added
3. target scripts/docs/tests
4. targeted validation
5. full validation
6. release state unchanged
7. generated-file exclusion
8. commit hash
9. draft PR URL
```
