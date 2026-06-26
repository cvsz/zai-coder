# Prompt: Subagent Delegation and Runner Orchestration

```text
You are working locally in:

/home/zeazdev/zai-coder

Phase:
v0.1.4+ Implementation PR — Subagent Delegation and Runner Orchestration

Branch:
feat/v0.1.4-subagent-runner-orchestration

Goal:
Add a safe subagent delegation design and a local automated runner orchestration foundation. The first implementation must be deterministic, bounded, auditable, and conservative.

Critical rules:
- No version bump.
- No tag/release/asset mutation.
- No direct main commit.
- Do not spawn uncontrolled parallel processes.
- Do not bypass safe runner policies.
- Do not create persistent background workers.
- Do not commit generated runner outputs, logs, DBs, or traces.
- Stage exact files only.

Step 1: Sync baseline

cd /home/zeazdev/zai-coder

git fetch origin --prune --tags
git switch main
git pull --ff-only origin main
git status --short

git switch -c feat/v0.1.4-subagent-runner-orchestration

Step 2: Inspect current orchestrator and agents

grep -R "MultiAgentOrchestrator\|build_agent\|agent\|orchestrator\|plan\|runner\|delegate" -n zai_coder tests docs assets 2>/dev/null | head -600

Step 3: Add runner data model

Recommended files:
- zai_coder/core/runner.py
- tests/test_runner_model_v014.py
- docs/architecture/agent-runner-model.md

Runner model:
- run_id
- parent_run_id optional
- task
- agent_name
- toolset/profile
- workspace
- status: pending, running, blocked, completed, failed
- max_steps
- timeout_seconds
- created_at
- completed_at
- summary

Step 4: Add delegation planner foundation

Recommended files:
- zai_coder/core/delegation.py
- tests/test_delegation_v014.py
- docs/architecture/subagent-delegation.md

Delegation model:
- max_subagents default 3
- isolated context per child
- restricted toolset per child
- no shared mutable state by default
- parent collects child summaries only
- child output redacted before parent context injection

Do not implement uncontrolled concurrent execution in this PR. Start with dry-run planning and deterministic sequential runner execution.

Step 5: CLI integration if small

Optional commands:
- zai-coder runner plan "task"
- zai-coder runner run "task" --dry-run
- zai-coder delegate "task" --agents planner,coder,reviewer --dry-run

If CLI integration is too large, ship library + tests + docs first.

Step 6: Validation

python3 -m pytest tests/test_runner_model_v014.py tests/test_delegation_v014.py -q
python3 -m pytest -q
python3 -m compileall -q zai_coder
make repo-check
make secret-scan
make stage-manifest-check
./scripts/repo/check-generated-state.sh
./scripts/repo/check-ci-pytest-setup.sh

git status --short

Step 7: Stage exact files only

git add zai_coder/core/runner.py
git add zai_coder/core/delegation.py
git add tests/test_runner_model_v014.py
git add tests/test_delegation_v014.py
git add docs/architecture/agent-runner-model.md
git add docs/architecture/subagent-delegation.md

# Add exact CLI files only if changed.

Step 8: Commit and PR

git commit -S -m "feat: add subagent runner orchestration foundation"
git push -u origin feat/v0.1.4-subagent-runner-orchestration

gh pr create \
  --base main \
  --head feat/v0.1.4-subagent-runner-orchestration \
  --draft \
  --title "feat: add subagent runner orchestration foundation" \
  --body "Adds bounded, audit-safe runner and delegation foundations without enabling uncontrolled background execution."

Report:
1. branch
2. runner model fields
3. delegation safeguards
4. dry-run behavior
5. CLI integration yes/no
6. validation result
7. generated-file exclusion
8. commit hash
9. draft PR URL
```
