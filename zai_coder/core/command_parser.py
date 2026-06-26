import shlex

class CommandParseError(ValueError):
    pass

class CommandParser:
    def __init__(self, workspace: str, timeout: int = 180, env: dict | None = None):
        self.workspace = workspace
        self.timeout = timeout
        self.env = env or {}

    def parse(self, command: str) -> dict:
        try:
            args = shlex.split(command)
        except ValueError as e:
            raise CommandParseError(f"Failed to parse command: {e}")

        if not args:
            raise CommandParseError("Empty command")

        name = args[0]
        
        # Check for shell metacharacter abuse and bypass patterns
        dangerous_tokens = {";", "|", "&&", "||", "&", ">", ">>", "<", "<<", "$(", "`"}
        for token in args:
            if token in dangerous_tokens:
                raise CommandParseError(f"Shell bypass token blocked: {token}")
                
        # Also check for inline command substitutions that shlex might leave together
        for token in args:
            if "$(" in token or "`" in token:
                raise CommandParseError(f"Shell substitution blocked in token: {token}")

        # Explicit blocks
        if name == "git" and len(args) > 1:
            if args[1] == "add" and any(arg in {".", "-A", "--all"} for arg in args[2:]):
                raise CommandParseError("Blocked: use exact-path staging, not git add all")
            if args[1] == "commit" and "--no-verify" in args:
                raise CommandParseError("Blocked: --no-verify bypasses checks")
            if args[1] == "push" and any(arg in {"-f", "--force", "--force-with-lease"} for arg in args):
                raise CommandParseError("Blocked: force push is disabled")
                
        if name == "rm" and "-rf" in args and any(arg in {"/", ".", "~", "$HOME"} for arg in args):
            raise CommandParseError("Blocked: broad rm -rf is dangerous")
            
        if name == "sudo" and len(args) > 1 and args[1] == "rm" and "-rf" in args and "/" in args:
            raise CommandParseError("Blocked: sudo rm -rf requires manual review")
            
        if name == "chmod" and "-R" in args and "777" in args:
            raise CommandParseError("Blocked: recursive chmod 777 is unsafe")
            
        if name in {"curl", "wget"} and any(arg.startswith("-") for arg in args) and "|" in command:
            # We already block |, but just to be sure
            raise CommandParseError("Blocked: remote execution")
            
        if ".env" in command and (name in {"cat", "echo", "python", "python3"}):
            raise CommandParseError("Blocked: revealing secrets")
                
        return {
            "name": name,
            "args": args,
            "cwd": self.workspace,
            "timeout": self.timeout,
            "env": self.env
        }
