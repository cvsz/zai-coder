# Local Scheduler Foundation

ZAI Coder includes a local scheduler foundation for running scheduled background tasks. By default, the scheduler relies on local cron syntax and remains completely disabled unless explicitly enabled.

## Jobs Data Model

Scheduled jobs are stored in `.zai-coder/tasks/scheduler.db` (or a designated path) using SQLite.
Properties include:
- `id`: Unique identifier
- `name`: Descriptive name for the job
- `command`: The command to run
- `schedule`: Cron expression
- `enabled`: Boolean status (default: false)
- `profile`: Safety profile / Toolset reference
- `created_at`: Job creation timestamp
- `last_run_at`: Timestamp of the last execution
- `last_result`: Output or status of the last execution

## Safety Constraints

- No resident daemon or autostart process runs in the background automatically.
- Jobs execute in dry-run mode until explicitly invoked or the scheduler runner is explicitly started.
- All scheduled executions pass through the SafetyPolicy.

## CLI Usage (Optional/Upcoming)

```bash
# List jobs
zai-coder schedule list

# Add a job (disabled by default)
zai-coder schedule add --name "audit" --cron "0 0 * * *" --command "make audit"

# Enable/Disable a job
zai-coder schedule enable <id>
zai-coder schedule disable <id>

# Run immediately in dry-run mode
zai-coder schedule run-now <id> --dry-run
```
