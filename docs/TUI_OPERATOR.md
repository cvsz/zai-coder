# TUI Operator Workflows

ZAI Coder supports an optional Terminal User Interface (TUI) powered by Textual. The TUI acts as an operator's dashboard connecting to local systems synchronously and presenting local data without spinning up complex local front-end servers.

## Features
- **Graceful Textual Fallbacks**: If `textual` isn't installed in the environment, the TUI templates fallback into static markdown rendering using standard print streams.
- **Dry-run Integration**: Directly checks command validity paths bounding external impacts securely inside dry-run schemas. 
- **Real-Time Dashboards**: Uses localized hooks into database models pulling local server health statuses and active task queue processes. 

## CLI Usage

```bash
# Check current template configs
./run.sh tui --print-config

# Review templates natively available
./run.sh tui --list-templates

# Run a specific dashboard in dry-run mode (does not require Textual)
./run.sh tui --template command-center --dry-run
./run.sh tui --template agent-hub --dry-run
./run.sh tui --template operation-gate --dry-run
```

## Security Profile
The operator panels map strictly to internal `zai_coder.core` operations via the `TuiIntegrations` middleware. The outputs ensure visual components have read-only access natively, explicitly prohibiting any sudo escalations. 
