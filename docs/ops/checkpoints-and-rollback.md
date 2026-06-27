# Checkpoints and Rollback

ZAI Coder supports checkpointing project states during patch applications and manual operations. This allows operators to easily rollback to a known good state.

## Listing Checkpoints

Checkpoints are stored in `.zai-coder/checkpoints` directory inside your workspace.

```bash
# Optional CLI command to list checkpoints
zai-coder checkpoint list
```

## Restoring Checkpoints

Restoring a checkpoint copies the files from the checkpoint directory back to their original locations in the workspace.

```bash
# Dry-run is the default
zai-coder checkpoint restore <id> --dry-run

# Apply the rollback
zai-coder checkpoint restore <id> --apply
```

## Safety Constraints

- Path traversal is blocked.
- Cannot restore over secret files (like `.env`) without explicit manual flags.
- Checkpoints are excluded from Git commits.
