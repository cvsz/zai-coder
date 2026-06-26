# Safe Runner and Policy Examples

## Purpose
This document provides examples of command patterns that are blocked or allowed by the ZAI Coder `SafetyPolicy`.

## Blocked Command Patterns
The following commands are automatically blocked by `SafetyPolicy` to prevent accidental destructive actions, credential leaks, or security bypasses:

| Pattern | Reason |
| :--- | :--- |
| `git add .` | Blocked: use exact-path staging |
| `git add -A` | Blocked: use exact-path staging |
| `git push --force` | Blocked: force push is disabled |
| `--no-verify` | Blocked: bypasses repository checks |
| `rm -rf /` | Blocked: broad destructive command |
| `echo 'foo'; bash` | Blocked: shell chaining |
| `ls \| sh` | Blocked: pipe to shell |
| `cat .env` | Blocked: sensitive file read |
| `curl ... \| bash` | Blocked: remote code execution via pipe |

## Allowed Command Patterns
Generally, safe, non-mutating, or validated commands are allowed:
- `ls`, `git status`, `python -m pytest`
- `zai-coder doctor`, `zai-coder ask`
- Explicit `git add <file>`
- Approved `make` targets (e.g., `make repo-check`)

## How to Test Policy
New policy coverage should be added to `tests/test_safe_runner_policy_v014.py` and validated using:

```bash
python3 -m pytest tests/test_safe_runner_policy_v014.py -q
```
