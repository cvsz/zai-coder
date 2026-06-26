import sys
from typing import Any

def prompt_for_approval(action_description: str) -> bool:
    print(f"\n[APPROVAL REQUIRED] {action_description}")
    try:
        response = input("Proceed? (y/N): ").strip().lower()
        return response in ["y", "yes"]
    except (EOFError, KeyboardInterrupt):
        return False

class ActionApprover:
    def __init__(self, apply_mode: bool = False):
        self.apply_mode = apply_mode

    def requires_approval(self, action: str) -> bool:
        risky_actions = ["run_command", "write_file", "delete_file"]
        return action in risky_actions

    def check(self, action: str, details: str) -> bool:
        if not self.apply_mode:
            print(f"[DRY RUN] Would execute: {action} - {details}")
            return False
            
        if self.requires_approval(action):
            return prompt_for_approval(f"{action}: {details}")
            
        return True
