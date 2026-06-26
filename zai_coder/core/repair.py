from pathlib import Path
from .patcher import PatchRuntime
from .safety import SafetyPolicy

class RepairManager:
    def __init__(self, workspace: str | Path):
        self.workspace = Path(workspace).resolve()
        self.checkpoint_dir = self.workspace / ".zai-coder" / "checkpoints"
        self.patcher = PatchRuntime(self.workspace, self.checkpoint_dir, SafetyPolicy(allow_apps_zlms=True))

    def check_patch(self, diff_text: str) -> bool:
        res = self.patcher.apply(diff_text, check_only=True)
        if not res.ok:
            print(f"Patch check failed: {res.blocked_reason or res.stderr}")
            return False
        return True

    def apply_patch(self, diff_text: str) -> bool:
        res = self.patcher.apply(diff_text, check_only=False)
        if not res.ok:
            print(f"Patch apply failed: {res.blocked_reason or res.stderr}")
            return False
        print(f"Patch applied successfully. Checkpoint: {res.checkpoint}")
        return True
