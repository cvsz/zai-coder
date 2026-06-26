import json
from pathlib import Path

def _load_manifest(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text())
    except Exception:
        return {}

def check_update(workspace: str, local_manifest_path: str) -> dict:
    installed_manifest = Path(workspace) / "dist" / "RELEASE_MANIFEST.json"
    local_manifest = Path(local_manifest_path)
    
    current = _load_manifest(installed_manifest)
    target = _load_manifest(local_manifest)
    
    current_version = current.get("version", "0.0.0")
    target_version = target.get("version", "0.0.0")
    
    can_update = target_version > current_version
    
    return {
        "current_version": current_version,
        "target_version": target_version,
        "can_update": can_update,
    }

def plan_update(workspace: str, local_manifest_path: str) -> dict:
    status = check_update(workspace, local_manifest_path)
    return {
        "status": status,
        "steps": [
            "1. Backup workspace data",
            "2. Apply SQLite migrations",
            "3. Replace python package files",
            "4. Verify post-install integrity"
        ] if status["can_update"] else ["Already up to date."]
    }
