# Operation Gate

`tui-template-06` / `operation-gate` is the approval-gate and release-gate workflow surface.

## Gate Pipeline

- Plan
- Dry Run
- Review
- Approval
- Apply
- Verify
- Rollback

Each gate tracks status, required evidence, command plan, and approval state. `ctrl+a` approves a dry-run result only. It does not run `APPLY=1`.

## Keyboard

- `q`: quit
- `ctrl+k`: command palette
- `ctrl+a`: approve dry-run result only
- `ctrl+r`: refresh
- `f1`: help
