# Full Project Requirements — ZAI Coder Control Plane

## Product Vision

ZAI Coder Control Plane is a local-first AI software and creative automation platform for developers, builders, and AI-native teams. It combines safe code operations, multi-agent workflows, project memory, creative automation, and GitHub/GPG release tooling.

## Non-Negotiable Requirements

1. Dry-run by default.
2. `APPLY=1` required for mutation.
3. No `git add .`.
4. No `git add -A`.
5. No `--no-verify`.
6. No force push.
7. No `apps/zlms/**`.
8. No secrets or `.env`.
9. No generated caches or build artifacts.
10. GPG signing supported but never stores passphrases.
11. GitHub CLI workflow must be explicit and reversible.
12. Every dangerous action must have a plan/check mode.

## Core Requirements

### CLI

- `doctor`
- `ask`
- `chat`
- `plan`
- `run`
- `self`
- future: `workspace`, `members`, `github`, `release`

### Agent System

- planner
- coder
- reviewer
- tester
- security
- devops
- docs
- media
- product
- supervisor

### Skill System

- file scan
- safe command run
- git status/diff
- patch check/apply
- memory
- audit log
- project scan
- media generation fallback
- GitHub release automation

### Members System

- roles
- permissions
- local SQLite storage
- invites
- future workspace mapping

### Creative System

- game core
- document core
- movie system
- asset library
- approval workflow
- export plan adapters

### GitHub System

- repo creation script using `gh`
- exact-path staging
- GPG signed commit
- GPG signed tag
- GitHub release creation
- issue templates
- PR template
- CI workflow
- safe release checklist

## Acceptance Criteria

```bash
python3 -m pytest -q
make doctor
make test
make scan
make github-plan
make gpg-doctor
```

All must complete without unsafe mutation.

## Packaging Requirements

- no `.git`
- no `.env`
- no `node_modules`
- no `dist`
- no `.next`
- no `coverage`
- no `reports`
- no `__pycache__`
- no `.pytest_cache`
- no private keys
- no API keys
