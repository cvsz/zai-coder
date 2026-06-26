---
name: repository-hardening-and-policy-update
description: Workflow command scaffold for repository-hardening-and-policy-update in zai-coder.
allowed_tools: ["Bash", "Read", "Write", "Grep", "Glob"]
---

# /repository-hardening-and-policy-update

Use this workflow when working on **repository-hardening-and-policy-update** in `zai-coder`.

## Goal

Improves repository security, readiness, and policy enforcement by updating CI, scripts, and policy modules.

## Common Files

- `.github/workflows/*.yml`
- `scripts/repo/*.sh`
- `zai_coder/github_ready_core/*.py`
- `tests/test_*.py`

## Suggested Sequence

1. Understand the current state and failure mode before editing.
2. Make the smallest coherent change that satisfies the workflow goal.
3. Run the most relevant verification for touched files.
4. Summarize what changed and what still needs review.

## Typical Commit Signals

- Update .github/workflows/ci.yml to add or modify CI steps.
- Modify or add scripts in scripts/repo/ and related directories.
- Update or add core policy/check modules (e.g., repo_check.py, repo_policy.py, secret_scan.py).
- Add or update tests to cover new checks or policies.

## Notes

- Treat this as a scaffold, not a hard-coded script.
- Update the command if the workflow evolves materially.