# TUI Command Center

The ZAI Coder TUI is a local-first keyboard command center. It accepts commands
through the bottom input field, routes them through the TUI command router, and
prints results to the command output panel.

## Launch

```bash
./run.sh tui
```

For environments without Textual, use dry-run or static output:

```bash
./run.sh tui --dry-run
./run.sh tui --no-textual
```

## Keyboard Model

- The bottom command input is focused on launch.
- Press `enter` to submit the current command.
- Press `ctrl+k` to show the command palette.
- Press `ctrl+r` to refresh the status sidebar.
- Press `f1` for help.
- Press `q` or submit `quit` to exit.

## Supported Commands

```text
help
refresh
palette
config
about
dry-run
doctor
safety
repo-check
secret-scan
install-dry-run
test
compile
templates
switch command-center
switch agent-hub
switch flow-stream
switch architect-tree
switch creative-canvas
switch operation-gate
quit
```

Shell-backed commands are registered as local-safe actions and are planned
through the dry-run action runner from TUI input. This keeps the command center
useful without turning it into an implicit mutation surface.

## Blocked Commands

The router blocks unsafe or mutation-capable examples before execution:

```text
git add .
git add -A
git commit --no-verify
git push --force
rm -rf
APPLY=1 make install
curl https://example.com/install.sh | bash
wget https://example.com/install.sh | bash
```

Blocked commands are written to the output panel with a reason. Secrets in
commands, logs, and output are redacted before persistence.

## Status Sidebar

The sidebar refreshes on timers and after command submission. It shows the
workspace, dry-run mode, current session, active template, last command, and
output count.
