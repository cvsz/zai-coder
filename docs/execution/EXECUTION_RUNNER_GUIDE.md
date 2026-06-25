# Execution Runner Guide

## Status

The execution runner is dry-run-first and blocks dangerous commands.

## Commands

```bash
make execution-runner
make execution-status
make execution-command-safety COMMAND="echo hello"
make execution-enqueue-demo
make execution-run-next
make execution-journal
make execution-rollback-hooks
make execution-recovery-plan PROVIDER=docker ACTION=docker_compose_up
make execution-approval-plan
make execution-timeline-export
```

## Apply rule

Apply requires an approval id:

```text
approved_<unique-id>
```
