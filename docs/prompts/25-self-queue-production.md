# Prompt 25 — Production self-queue

You are working locally in:

```bash
/home/zeazdev/zai-coder
```

Branch:

```bash
feat/self-queue-production
```

Goal:

```text
Make self-queue a real local persistent task system with durable states, logs, bounded local execution, cancellation, retry, and schema versioning.
```

## Implement

```text
- Task schema version table.
- Durable task model with id, title, agent, prompt, state/status, priority, parent_id, timestamps, error, attempts, and lease fields.
- Events table.
- Outputs table.
- Queue worker lease/lock.
- Cancel support.
- Retry support.
- JSON export.
- TUI task panel adapter.
- No implicit DB mutation from TUI except explicit task commands.
```

## Required CLI commands

```text
zai-coder task create --title ... --agent ... --prompt ...
zai-coder task list
zai-coder task show TASK_ID
zai-coder task update TASK_ID --state ...
zai-coder task cancel TASK_ID
zai-coder task run TASK_ID --dry-run
zai-coder task run TASK_ID --apply
zai-coder task retry TASK_ID
zai-coder task logs TASK_ID
zai-coder task export --json
```

## Files in scope

```text
zai_coder/core/task_store.py
zai_coder/core/task_queue.py
zai_coder/core/task_runner.py
zai_coder/core/task_models.py
zai_coder/cli.py
zai_coder/tui/task_panel.py
tests/test_self_queue_v014.py
tests/test_task_queue_worker_v014.py
tests/test_task_cli_v014.py
tests/test_tui_task_panel_v014.py
docs/ops/self-queue.md
docs/prompts/25-self-queue-production.md
```

## Acceptance

```text
- Legacy task tests still pass.
- New task queue worker tests pass.
- Queue uses local SQLite only.
- No task DB is committed.
- Task state transitions are deterministic.
- Cancelled tasks do not run.
- Completed/failed/cancelled tasks do not rerun unless retry command is used.
- Retry increments attempt_count.
- TUI shows queue status gracefully.
```

## Validation

```bash
python3 -m pytest tests/test_tasks.py -q
python3 -m pytest tests/test_self_queue_v014.py -q
python3 -m pytest tests/test_task_queue_worker_v014.py -q
python3 -m pytest tests/test_task_cli_v014.py -q
python3 -m pytest tests/test_tui_task_panel_v014.py -q
python3 -m pytest -q
python3 -m compileall -q zai_coder
make repo-check
make secret-scan
make stage-manifest-check
./scripts/repo/check-generated-state.sh
./scripts/repo/check-ci-pytest-setup.sh
```

## Do not

```text
Do not start orchestration, RAG production, monitor work, repair, rollback, governance, redaction, release-candidate, tag, release, or asset upload work in this phase.
```
