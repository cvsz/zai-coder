# ZAI Coder Full Master Advanced Professional Final Release

## Multi-Agent Implementation Prompt — Release-Safe Baseline

Repository:

```text
cvsz/zai-coder
```

Local path:

```bash
/home/zeazdev/zai-coder
```

Public command:

```text
zai-coder
```

Python import/package name:

```text
zai_coder
```

Never rename Python imports or directories from `zai_coder` to `zai-coder`.

## Current baseline

```text
- Current package version: 0.1.3
- Stable release: v0.1.3
- TUI command center and palette work are merged through PR #34
- Open PR queue should be empty before starting the next phase
- Next implementation phase: feat/self-queue-production
```

## Safety rules

```text
Do not push directly to main.
Do not force push.
Do not rewrite history.
Do not use git add .
Do not use git add -A.
Do not use --no-verify.
Do not use --break-system-packages.
Do not run curl | bash.
Do not run wget | bash.
Do not commit secrets.
Do not commit .env.
Do not commit virtualenvs, caches, reports, release assets, runtime DBs, logs, generated state, checkpoints, SQLite DBs, or local artifacts.
All risky actions must be dry-run-first.
All mutation-capable flows must require explicit operator approval.
All shell commands launched by ZAI Coder must pass SafetyPolicy.
Use exact-file staging only.
```

## Multi-agent roles

```text
Supervisor Agent: phase objective, branch, scope, acceptance criteria.
Architect Agent: data model, modules, CLI/TUI, safety contracts.
Coder Agent: focused implementation only.
Test Agent: targeted + regression tests.
Security Agent: SafetyPolicy, redaction, generated-state, secrets.
Docs Agent: docs/ops, docs/prompts, runbooks.
Reviewer Agent: scope, diff, safety, naming.
Release Gate Agent: validation + PR report.
```

## Required PR report

```text
1. Branch
2. Base main commit
3. Files changed
4. Features implemented
5. Safety gates preserved
6. Tests added/updated
7. Targeted validation
8. Full validation
9. Generated-state check
10. Commit hash
11. Draft PR URL
12. Next recommended PR
```
