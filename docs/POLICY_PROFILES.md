# Policy Governance Profiles

ZAI Coder uses JSON-based governance profiles to restrict the actions and paths available to the AI.

## Built-in Profiles

- `read_only`: Inspect only. Denies state mutation.
- `developer`: Local development and testing. Allows full file access and execution except destructive actions.
- `release`: Package and release checks. Restricts to read access and build tools.
- `operator`: Local runtime operations.
- `locked_down`: Denies all risky actions.

## Policy Schema

Each policy JSON contains:
- `name`: string
- `description`: string
- `allowed_commands`: list of exact commands allowed to run
- `denied_patterns`: list of regex patterns blocking specific command structures
- `protected_paths`: list of directories or files completely blocked from access
- `generated_paths`: list of directories ignored as they contain noisy build artifacts
- `max_timeout_seconds`: maximum execution time for processes
- `require_approval`: boolean for gating execution
- `allow_network`: boolean for controlling egress
- `allow_shell`: boolean for shell substitution
- `allow_write`: boolean for writing files

## Integration
Policies are stored in `assets/policies/`. If missing, the engine falls back to hardcoded defaults in `policy_loader.py`.
