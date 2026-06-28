# Agent Runner Model

The Agent Runner Model orchestrates the execution of tasks assigned to specific agents.

## Core Properties

- **run_id**: Unique identifier for the run.
- **parent_run_id**: Optional ID of the parent run, establishing hierarchy.
- **task**: The objective or instruction.
- **agent_name**: The assigned agent profile (e.g., coder, reviewer).
- **toolset/profile**: Restricted toolset boundary (default: `default`).
- **workspace**: Sandboxed workspace directory.
- **status**: Current state (`pending`, `running`, `blocked`, `completed`, `failed`).
- **max_steps**: Step limits (default 50).
- **timeout_seconds**: Execution timeout (default 3600s).
- **created_at** / **completed_at**: Lifecycle timestamps.
- **summary**: The resulting summary of the execution.

## Execution Model

In the current v0.1.4 foundation, the runner operates deterministically and sequentially. Background daemon workers are not enabled by default to ensure maximum auditability and bounds control.
