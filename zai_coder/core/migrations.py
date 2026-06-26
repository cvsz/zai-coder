import sqlite3
import shutil
import time
import importlib
import pkgutil
from pathlib import Path
import zai_coder.migrations

class MigrationManager:
    def __init__(self, workspace: str = "."):
        self.workspace = Path(workspace).expanduser().resolve()
        self.db_path = self.workspace / "data" / "migrations.db"
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(str(self.db_path))
        self._init_db()

    def _init_db(self):
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS applied_migrations (
                    id TEXT PRIMARY KEY,
                    applied_at REAL
                )
            """)

    def _get_applied(self) -> set[str]:
        cur = self.conn.execute("SELECT id FROM applied_migrations")
        return {row[0] for row in cur.fetchall()}

    def _get_available(self) -> list[str]:
        available = []
        for _, name, _ in pkgutil.iter_modules(zai_coder.migrations.__path__):
            available.append(name)
        return sorted(available)

    def status(self) -> dict:
        applied = self._get_applied()
        available = self._get_available()
        pending = [m for m in available if m not in applied]
        return {
            "applied": list(applied),
            "available": available,
            "pending": pending
        }

    def _backup(self):
        backup_dir = self.workspace / "data" / "backups" / f"pre_migrate_{int(time.time())}"
        backup_dir.mkdir(parents=True, exist_ok=True)
        # Just backup the DBs for now to simulate a fast local state backup
        if self.db_path.exists():
            shutil.copy2(self.db_path, backup_dir / "migrations.db")
        tasks_db = self.workspace / "data" / "tasks.db"
        if tasks_db.exists():
            shutil.copy2(tasks_db, backup_dir / "tasks.db")
        return backup_dir

    def apply(self, dry_run: bool = True) -> list[str]:
        applied = self._get_applied()
        available = self._get_available()
        pending = [m for m in available if m not in applied]
        
        if not pending:
            return []

        if not dry_run:
            self._backup()

        results = []
        for m in pending:
            mod = importlib.import_module(f"zai_coder.migrations.{m}")
            if hasattr(mod, "up"):
                if dry_run:
                    results.append(f"[DRY RUN] Would apply {m}")
                else:
                    mod.up(self.conn)
                    with self.conn:
                        self.conn.execute("INSERT INTO applied_migrations (id, applied_at) VALUES (?, ?)", (m, time.time()))
                    results.append(f"Applied {m}")
            else:
                results.append(f"Skipped {m} (no up() function)")
        return results
