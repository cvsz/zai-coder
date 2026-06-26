import hashlib
from pathlib import Path

def get_file_fingerprint(filepath: str | Path) -> str:
    path = Path(filepath)
    if not path.is_file():
        return ""
    
    sha256 = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(65536), b""):
            sha256.update(block)
    return sha256.hexdigest()

def should_ignore_file(filepath: str | Path) -> bool:
    p = Path(filepath).resolve()
    parts = p.parts
    ignore_dirs = {
        ".git", ".venv", "venv", "__pycache__", ".pytest_cache", 
        "node_modules", "dist", "build", ".next", "coverage", 
        "reports", "out"
    }
    for part in parts:
        if part in ignore_dirs:
            return True
            
    name = p.name.lower()
    if name.endswith((".zip", ".tar", ".tgz", ".gz", ".db", ".sqlite", ".sqlite3")):
        return True
        
    if name == ".env" or "secret" in name or "token" in name or name.endswith(".key"):
        return True
        
    return False
