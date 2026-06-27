# Self Queue

`zai-coder task` provides the local persistent task queue used by the self-queue phase.

## Storage

- SQLite database: `.zai-coder/tasks/tasks.db`
- Schema version table: `schema_version`
- Task tables: `tasks`, `task_events`, `task_outputs`

## States

- `queued`
- `running`
- `waiting_approval`
- `completed`
- `failed`
- `cancelled`

## Commands

```bash
./zai-coder task create --title "scan repo" --agent planner --prompt "inspect the tree"
./zai-coder task list
./zai-coder task show TASK_ID
./zai-coder task update TASK_ID --state running
./zai-coder task cancel TASK_ID
./zai-coder task run TASK_ID --dry-run
./zai-coder task run TASK_ID --apply
./zai-coder task retry TASK_ID
./zai-coder task logs TASK_ID
./zai-coder task export --json
```

## Behavior

- Dry-run execution marks the task cancelled without performing local mutation.
- Apply execution requires approval for risky command paths.
- Retry returns a failed or cancelled task to `queued` and clears lease ownership.
- Queue workers lease the next queued task with a bounded lease window.
- The TUI task panel reads the queue in read-only mode and does not mutate the database.

