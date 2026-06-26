# Self-Heal and Repair Workflow

ZAI Coder introduces an automated Self-Heal workflow allowing for proactive detection, planning, and safe remediation of failures.

## Features
- **Failure Parsing**: Detects assertion outputs (`pytest`), python syntax issues (`compileall`), and command failures dynamically.
- **Repair Plans**: Structurally decomposes error traces to propose explicit context chunks and prompt sequences.
- **Dry-Run Validation**: Safely assesses `.diff` compatibility without executing writes.
- **Automated Checkpoints**: Creates timestamped back-ups inside `.zai-coder/checkpoints` prior to finalizing any patch logic.
- **Artifact Protection**: Implicit safety blocks modifications to `.env` or temporary system-generated directories.

## CLI Usage

```bash
# Check current environment for failures dynamically
./zai-coder self heal --check

# Generate a repair plan directly from a specific output log
./zai-coder self heal --from-log out/pytest.log

# Evaluate a generated patch for applicability
./zai-coder repair check out/fix.diff

# Apply the patch with mandatory approval and checkpointing
./zai-coder repair apply out/fix.diff --apply
```
