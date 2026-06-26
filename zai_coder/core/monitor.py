import sys
import platform
import shutil
import socket
import json
from pathlib import Path

class SystemMonitor:
    def __init__(self, workspace: str | Path):
        self.workspace = Path(workspace).resolve()

    def check_ollama(self) -> bool:
        try:
            with socket.create_connection(("127.0.0.1", 11434), timeout=0.5):
                return True
        except OSError:
            return False

    def get_disk_usage(self) -> dict:
        total, used, free = shutil.disk_usage(self.workspace)
        return {
            "total_gb": round(total / (1024**3), 2),
            "used_gb": round(used / (1024**3), 2),
            "free_gb": round(free / (1024**3), 2),
        }

    def check_db_health(self, path: Path) -> dict:
        if not path.exists():
            return {"status": "missing"}
        
        import sqlite3
        try:
            with sqlite3.connect(f"file:{path}?mode=ro", uri=True) as conn:
                conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
            return {"status": "ok", "size_bytes": path.stat().st_size}
        except Exception as e:
            return {"status": "error", "error": str(e)}

    def check_audit_log(self, path: Path) -> dict:
        if not path.exists():
            return {"status": "missing"}
        return {"status": "ok", "size_bytes": path.stat().st_size}

    def check_package_health(self) -> str:
        try:
            import zai_coder
            return "ok"
        except ImportError:
            return "error"
            
    def check_config_health(self) -> str:
        cfg_path = self.workspace / ".zai-coder" / "config.json"
        if not cfg_path.exists():
            return "default"
        try:
            json.loads(cfg_path.read_text())
            return "ok"
        except json.JSONDecodeError:
            return "error"

    def get_recent_failures(self) -> int:
        # Just a mock or a parse of some known log file.
        # We can return 0 if no clear way to parse without executing things.
        return 0

    def get_snapshot(self) -> dict:
        return {
            "python_version": sys.version.split()[0],
            "platform": platform.platform(),
            "disk_usage": self.get_disk_usage(),
            "ollama_available": self.check_ollama(),
            "package_health": self.check_package_health(),
            "config_health": self.check_config_health(),
            "task_db": self.check_db_health(self.workspace / ".zai-coder" / "tasks" / "tasks.db"),
            "index_db": self.check_db_health(self.workspace / ".zai-coder" / "index" / "project-index.db"),
            "audit_log": self.check_audit_log(self.workspace / "data" / "zai-audit.jsonl"),
            "recent_failures": self.get_recent_failures()
        }
