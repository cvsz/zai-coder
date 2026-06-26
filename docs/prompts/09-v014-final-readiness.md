# Prompt: v0.1.4 Final Readiness

```text
You are working locally in:

/home/zeazdev/zai-coder

Phase:
v0.1.4 Final Readiness — Pre-Release Candidate Docs and Gate Review

Branch:
chore/v0.1.4-final-readiness

Goal:
After v0.1.4 implementation PRs are merged, prepare final readiness documentation and verify release gates before a release candidate branch exists. Do not bump version yet.

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
git switch -c chore/v0.1.4-final-readiness

Verify baseline:

python3 -m compileall -q zai_coder
python3 -m pytest -q
make repo-check
make secret-scan
make stage-manifest-check
make package APPLY=1
make package-check
./scripts/repo/check-generated-state.sh
./scripts/repo/check-ci-pytest-setup.sh

Create:
- docs/release/V0.1.4_FINAL_READINESS.md
- docs/release/V0.1.4_RELEASE_GATE_CHECKLIST.md
- docs/release/RELEASE_NOTES_v0.1.4_DRAFT.md

Content requirements:
- summarize completed v0.1.4 implementation PRs
- list validation results
- list release candidate stop conditions
- explicitly mark version bump/tag/release/upload as not done
- state package artifacts are local-only if generated

Generated-file exclusion check:

git status --short
git ls-files dist .zai-coder .pytest_cache status.txt data/*.db data/**/*.db '*.sqlite' '*.sqlite3' 2>/dev/null || true

git add docs/release/V0.1.4_FINAL_READINESS.md
git add docs/release/V0.1.4_RELEASE_GATE_CHECKLIST.md
git add docs/release/RELEASE_NOTES_v0.1.4_DRAFT.md
git commit -S -m "chore: prepare v0.1.4 final readiness"
git push -u origin chore/v0.1.4-final-readiness

gh pr create \
  --base main \
  --head chore/v0.1.4-final-readiness \
  --draft \
  --title "chore: prepare v0.1.4 final readiness" \
  --body-file docs/release/V0.1.4_FINAL_READINESS.md

Report:
1. branch
2. main baseline
3. validation result
4. docs created
5. version still pre-release
6. tag/release not created
7. generated-file exclusion
8. commit hash
9. draft PR URL
```
