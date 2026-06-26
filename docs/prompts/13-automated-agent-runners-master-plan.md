# Prompt: Automated Agent Runners Master Plan

```text
You are working locally in:

/home/zeazdev/zai-coder

Phase:
v0.1.4+ Planning PR — Automated Agent Runners Master Plan

Branch:
docs/automated-agent-runners-master-plan

Goal:
Create an audit-safe implementation plan for automated agent runners, toolsets, skills, context loading, memory, checkpoints, scheduler, delegation, provider routing, integrations, and product feature claims. This phase is documentation/planning only.

Current baseline:
- v0.1.3 release is complete.
- PR #21 generated-state guardrails merged.
- PR #22 release-process guardrails merged.
- PR #23 v0.1.4 planning baseline merged.
- PR #25 CLI diagnostics merged.
- PR #26 CLI diagnostics platform portability hotfix merged.
- Current package version remains 0.1.3.
- Current expected validation after PR #26: 479 tests passed.

Critical rules:
- Do not bump version.
- Do not create tags.
- Do not publish or mutate GitHub releases.
- Do not upload release assets.
- Do not push directly to main.
- Do not force push.
- Do not use git add .
- Do not use git add -A
- Do not use --no-verify.
- Do not commit dist/, .zai-coder/, .pytest_cache/, runtime DBs, SQLite files, generated evidence/export JSON, status.txt, or runtime logs.
- Stage exact files only.
- This phase must not implement risky automation. It creates planning docs and prompt files only.

Step 1: Sync baseline

cd /home/zeazdev/zai-coder

git fetch origin --prune --tags
git switch main
git pull --ff-only origin main
git status --short
git log -20 --oneline --decorate

Step 2: Create branch

git switch -c docs/automated-agent-runners-master-plan

Step 3: Inspect current capability surface

grep -R "class ToolRuntime\|class SafetyPolicy\|class MemoryStore\|class LocalRAG\|PatchRuntime\|run_server\|ModelRouter\|provider_from_config\|cmd_" -n zai_coder tests docs scripts 2>/dev/null | head -500

find zai_coder -maxdepth 4 -type f | sort
find docs/prompts -maxdepth 1 -type f | sort

Step 4: Create docs/architecture/AUTOMATED_AGENT_RUNNERS_PLAN.md

Include these sections:
- Purpose
- Current baseline
- Current available capabilities
- Hermes-style feature alignment
- Feature statuses: available, partial, planned, requires_integration, do_not_claim
- Runner architecture
- Agent runner lifecycle
- Toolset model
- Safe execution model
- Memory model
- Context model
- Checkpoint and rollback model
- Scheduler model
- Delegation model
- Plugin and MCP model
- Provider routing model
- Product tiers and claim-control model
- Recommended PR sequence
- Validation gates
- Explicit non-goals

Step 5: Create docs/architecture/AUTOMATED_AGENT_RUNNERS_PR_SEQUENCE.md

Use this sequence:
1. Safe runner policy coverage.
2. Feature registry and claim-control matrix.
3. Toolsets registry.
4. Context files discovery.
5. Context references.
6. Checkpoint and rollback UX.
7. Local scheduler.
8. Subagent delegation plan.
9. Plugin registry foundation.
10. MCP adapter interface.
11. Provider routing improvements.
12. API server compatibility hardening.
13. Product docs and tier plan.

Step 6: Create docs/prompts index extension if needed

Update docs/prompts/README.md with links to any new prompt files added by this branch.

Step 7: Validation

python3 -m pytest -q
python3 -m compileall -q zai_coder
make repo-check
make secret-scan
make stage-manifest-check
./scripts/repo/check-generated-state.sh
./scripts/repo/check-ci-pytest-setup.sh

git status --short

Step 8: Stage exact files only

git add docs/architecture/AUTOMATED_AGENT_RUNNERS_PLAN.md
git add docs/architecture/AUTOMATED_AGENT_RUNNERS_PR_SEQUENCE.md
git add docs/prompts/README.md

# Add exact prompt files only if created.

Step 9: Commit and PR

git commit -S -m "docs: plan automated agent runners"
git push -u origin docs/automated-agent-runners-master-plan

gh pr create \
  --base main \
  --head docs/automated-agent-runners-master-plan \
  --draft \
  --title "docs: plan automated agent runners" \
  --body "Adds the automated agent runners master plan and PR sequence without changing release state."

Report:
1. branch
2. baseline main commit
3. files created
4. feature statuses documented
5. validation result
6. generated-file exclusion result
7. commit hash
8. draft PR URL
9. next recommended implementation PR
```
