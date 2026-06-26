# Prompt: v0.1.4 Safe Runner and Policy Hardening

```text
You are working locally in:

/home/zeazdev/zai-coder

Phase:
v0.1.4 Implementation PR — Safe Runner and Policy Hardening

Branch:
test/v0.1.4-safe-runner-policy

Goal:
Expand safe-runner and policy regression coverage for dangerous commands and improve blocked-command diagnostics where needed. Keep behavior safety-first and auditable.

Critical rules:
- No version bump.
- No tag/release/asset mutation.
- No direct main commit.
- Do not weaken safety policy.
- Do not add bypasses for dangerous commands.
- Do not commit generated state.
- Stage exact files only.

Steps:

cd /home/zeazdev/zai-coder

git fetch origin --prune --tags
git switch main
git pull --ff-only origin main
git status --short
git switch -c test/v0.1.4-safe-runner-policy

Inspect policy and runner code:

grep -R "SafetyPolicy\|safe runner\|blocked\|git add -A\|git add .\|--no-verify\|force push\|rm -rf" -n zai_coder tests docs scripts 2>/dev/null | head -420

Add tests for:
- git add .
- git add -A
- git commit --no-verify
- git push --force
- destructive shell chains
- broad rm/rmdir patterns
- secret/env file operations
- generated DB/evidence commit attempts if represented by policy

Recommended files:
- tests/test_safe_runner_policy_v014.py
- docs/ops/safe-runner-policy-examples.md
- existing safe runner/policy source only if diagnostics need improvement

Validation:

python3 -m pytest tests/test_safe_runner_policy_v014.py -q
python3 -m pytest -q
python3 -m compileall -q zai_coder
make repo-check
make secret-scan
make stage-manifest-check
./scripts/repo/check-generated-state.sh
./scripts/repo/check-ci-pytest-setup.sh

git status --short

git add tests/test_safe_runner_policy_v014.py
git add docs/ops/safe-runner-policy-examples.md
# add exact policy/source files only if changed

git commit -S -m "test: harden safe runner policy coverage"
git push -u origin test/v0.1.4-safe-runner-policy

gh pr create \
  --base main \
  --head test/v0.1.4-safe-runner-policy \
  --draft \
  --title "test: harden safe runner policy coverage" \
  --body "Expands v0.1.4 safe-runner and policy regression coverage without changing release state."

Report:
1. branch
2. baseline
3. policy cases covered
4. diagnostics changes if any
5. targeted validation
6. full validation
7. generated-file exclusion
8. commit hash
9. draft PR URL
```
