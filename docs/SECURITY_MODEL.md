# ZAI Coder Security Model

ZAI Coder implements an enterprise-grade safe command execution engine.

## Command Execution (ToolRuntime)
- Prefers `subprocess.run` with `shell=False`.
- Uses `shell=True` only for explicitly approved compatibility cases.
- Parses command into `argv` safely using `shlex`.
- Blocks shell metacharacter abuse (`;`, `|`, `&`, `>`).
- Blocks command chaining and substitution (`$()`, `` ` ``).
- Blocks pipe-to-shell patterns.
- Enforces workspace-contained `cwd`.
- Implements bounded timeouts.
- Implements max output size (1MB).
- Redacts secrets from stdout and stderr before returning or logging.
- Supports environment allowlist.
- Audits every command execution.

## Policy Governance
Commands are governed by strict profiles:
- `read_only`
- `test`
- `build`
- `patch`
- `operator`
- `locked_down`

## Safety Policy
Safety checks proactively block dangerous patterns before parsing:
- `git add .` / `git add -A` / `git add --all`
- `git commit --no-verify`
- `git push --force` / `git push --force-with-lease`
- `rm -rf /` / `rm -rf .` / `sudo rm -rf /`
- `chmod -R 777 .`
- Remote shell loading (e.g. `curl | bash`, `wget | sh`)
- Revealing secrets (`cat .env`, `echo $(cat .env)`)
