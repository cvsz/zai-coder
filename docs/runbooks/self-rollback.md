# Runbook: self-rollback

Restore a previous checkpoint and audit the rollback.

## Commands

```bash
./zai-coder checkpoint restore CHECKPOINT_ID
```

## Outputs

- restored files
- audit entry

## Safety

- explicit checkpoint id
- confirmation required
