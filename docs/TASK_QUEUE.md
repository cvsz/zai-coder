# Task Queue and Orchestration

ZAI Coder incorporates a fully local task queue to manage and persist agent orchestrations in `.zai-coder/tasks/tasks.db`.

## Features
- **States**: Track workflow steps (`queued`, `running`, `waiting_approval`, `completed`, `failed`, `cancelled`).
- **Events**: Write audit logs associated tightly to exact task states.
- **Dry-run**: Assumes simulation mode default; `--apply` enforces risky changes.
- **Local SQLite Storage**: Fast metadata storage.

## CLI Usage

```bash
# Create a new background task
./zai-coder task create --title "scan repo" --agent planner --prompt "inspect repo"

# List active and completed tasks
./zai-coder task list

# Show metadata for a task
./zai-coder task show TASK_ID

# Run task simulation
./zai-coder task run TASK_ID --dry-run

# Run and apply modifications
./zai-coder task run TASK_ID --apply

# Display execution event logs
./zai-coder task logs TASK_ID

# Stop a pending task
./zai-coder task cancel TASK_ID
```
