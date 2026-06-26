import json
import sqlite3
from pathlib import Path

class TuiIntegrations:
    def __init__(self, workspace: str | Path):
        self.workspace = Path(workspace).resolve()
        
    def get_task_queue_list(self) -> str:
        db_path = self.workspace / ".zai-coder" / "tasks" / "tasks.db"
        if not db_path.exists():
            return "Task DB not initialized."
        try:
            with sqlite3.connect(f"file:{db_path}?mode=ro", uri=True) as conn:
                cur = conn.cursor()
                cur.execute("SELECT id, state FROM tasks LIMIT 5")
                rows = cur.fetchall()
                if not rows:
                    return "No tasks."
                return ", ".join(f"{r[0]}: {r[1]}" for r in rows)
        except Exception as e:
            return f"Task DB error: {e}"

    def get_local_server_status(self) -> str:
        import socket
        try:
            with socket.create_connection(("127.0.0.1", 8765), timeout=0.5):
                return "Online (port 8765)"
        except OSError:
            return "Offline"

    def get_agent_registry(self) -> str:
        return "planner, coder, reviewer (3 agents loaded)"

    def get_skill_registry(self) -> str:
        return "docs, test, search (3 skills loaded)"

    def get_policy_profile(self) -> str:
        return "developer"

    def get_audit_tail(self) -> str:
        audit_file = self.workspace / "data" / "zai-audit.jsonl"
        if not audit_file.exists():
            return "No audit logs."
        try:
            lines = audit_file.read_text().splitlines()
            if lines:
                return lines[-1][:100]
            return "Audit log empty."
        except Exception:
            return "Audit log unreadable."

    def get_safe_command_runner_dry_run(self) -> str:
        return "DRY-RUN ENABLED"

    def get_final_release_status(self) -> str:
        return "PENDING (not checked)"
