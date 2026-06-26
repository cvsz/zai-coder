from typing import Set

PROFILES: dict[str, Set[str]] = {
    "read_only": {"ls", "cat", "grep", "find", "head", "tail"},
    "test": {"pytest", "python", "python3", "make", "npm", "yarn"},
    "build": {"make", "npm", "yarn", "docker", "cargo"},
    "patch": {"patch", "git", "diff"},
    "operator": {
        "ls", "cat", "grep", "find", "head", "tail",
        "pytest", "python", "python3", "make", "npm", "yarn",
        "docker", "cargo", "patch", "git", "diff",
        "bash", "sh", "chmod", "echo", "rm", "mkdir"
    },
    "locked_down": set()
}

def get_allowed_commands(profile_name: str) -> Set[str]:
    return PROFILES.get(profile_name, set())
