# Runbook: self-heal

Detect failed tests or broken commands, propose minimal patches, and require approval before apply.

## Commands

```bash
./zai-coder self heal --check
```

## Outputs

- fix plan
- candidate patch

## Safety

- dry-run first
- checkpoint before apply
- no destructive commands
