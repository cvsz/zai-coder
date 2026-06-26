# Prompt: v0.1.4 Operator Documentation Polish

```text
You are working locally in:

/home/zeazdev/zai-coder

Phase:
v0.1.4 Implementation PR — Operator Documentation and Examples Polish

Branch:
docs/v0.1.4-operator-docs

Goal:
Improve operator-facing documentation, examples, and docs navigation for local-first ZAI Coder usage. This phase should be docs-only unless a small metadata reference is needed.

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
git switch -c docs/v0.1.4-operator-docs

Inspect docs:

find docs -maxdepth 4 -type f | sort
sed -n '1,260p' README.md 2>/dev/null || true
grep -R "install\|diagnostic\|doctor\|release\|guardrail\|safe runner\|local-first\|troubleshoot" -n README.md docs 2>/dev/null | head -420

Create or update:
- docs/ops/README.md as an ops docs index if missing
- docs/ops/troubleshooting.md for common local issues
- docs/ops/cli-examples.md for common CLI examples
- README.md links only if needed

Validation:

python3 -m pytest -q
python3 -m compileall -q zai_coder
make repo-check
make secret-scan
make stage-manifest-check
./scripts/repo/check-generated-state.sh
./scripts/repo/check-ci-pytest-setup.sh

git status --short

git add docs/ops/README.md
git add docs/ops/troubleshooting.md
git add docs/ops/cli-examples.md
# git add README.md only if changed

git commit -S -m "docs: polish operator documentation"
git push -u origin docs/v0.1.4-operator-docs

gh pr create \
  --base main \
  --head docs/v0.1.4-operator-docs \
  --draft \
  --title "docs: polish operator documentation" \
  --body "Improves v0.1.4 operator docs, troubleshooting, and CLI examples without changing release state."

Report:
1. branch
2. docs changed
3. README changed yes/no
4. validation result
5. generated-file exclusion
6. commit hash
7. draft PR URL
```
