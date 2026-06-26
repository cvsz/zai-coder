# Prompt: v0.1.4 CLI Operator Diagnostics

```text
You are working locally in:

/home/zeazdev/zai-coder

Phase:
v0.1.4 Implementation PR — CLI Operator UX and Diagnostics

Branch:
chore/v0.1.4-cli-diagnostics

Goal:
Improve operator-facing CLI diagnostics while preserving existing behavior and local-first safety. Add or improve a diagnostics command only if the current CLI structure supports it cleanly. Otherwise, add planning docs, tests, and error-message improvements.

Critical rules:
- No version bump.
- No tag/release/asset mutation.
- No direct main commit.
- Do not commit generated state.
- Stage exact files only.

Steps:

cd /home/zeazdev/zai-coder

git fetch origin --prune --tags
git switch main
git pull --ff-only origin main
git status --short
git switch -c chore/v0.1.4-cli-diagnostics

Inspect CLI:

find zai_coder -maxdepth 3 -type f | sort | grep -E 'cli|command|diagnostic|doctor|config|runner' || true
grep -R "argparse\|click\|typer\|def main\|subcommand\|--version\|doctor\|diagnostic" -n zai_coder tests docs 2>/dev/null | head -320

Implement one focused improvement:
- add or improve `zai-coder doctor` if architecture supports it;
- or add environment/config diagnostics to existing CLI output;
- or add tests and docs for existing diagnostics.

Required tests:
- CLI help still passes.
- version output remains stable.
- diagnostics command or diagnostics path returns useful output.
- failure path does not mutate runtime state.

Recommended files:
- zai_coder/cli.py or relevant CLI module
- tests/test_cli_diagnostics_v014.py
- docs/ops/cli-diagnostics.md

Validation:

python3 -m pytest tests/test_cli_diagnostics_v014.py -q
python3 -m pytest -q
python3 -m compileall -q zai_coder
make repo-check
make secret-scan
make stage-manifest-check
./scripts/repo/check-generated-state.sh
./scripts/repo/check-ci-pytest-setup.sh

git status --short

git add <exact changed source files>
git add tests/test_cli_diagnostics_v014.py
git add docs/ops/cli-diagnostics.md
git commit -S -m "chore: improve CLI diagnostics"
git push -u origin chore/v0.1.4-cli-diagnostics

gh pr create \
  --base main \
  --head chore/v0.1.4-cli-diagnostics \
  --draft \
  --title "chore: improve CLI diagnostics" \
  --body "Improves operator-facing CLI diagnostics for v0.1.4 without changing release state."

Report:
1. branch
2. baseline
3. CLI improvement summary
4. tests added
5. validation result
6. generated-file exclusion result
7. commit hash
8. draft PR URL
```
