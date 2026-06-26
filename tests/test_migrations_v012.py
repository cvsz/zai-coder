import sqlite3
import pytest
from pathlib import Path
from zai_coder.app_studio.migrations import Migration, MigrationManager

def test_migration_dataclass():
    m = Migration(version="999", name="test_mig", sql="SELECT 1;")
    d = m.to_dict()
    assert d["version"] == "999"
    assert d["name"] == "test_mig"
    assert d["sql"] == "SELECT 1;"

def test_migration_manager_flow(tmp_path):
    db_file = tmp_path / "app_studio.db"
    
    test_migrations = [
        Migration(version="001", name="first", sql="CREATE TABLE t1 (id INTEGER PRIMARY KEY);"),
        Migration(version="002", name="second", sql="CREATE TABLE t2 (id INTEGER PRIMARY KEY);"),
    ]
    
    manager = MigrationManager(db_path=db_file, migrations=test_migrations)
    
    # 1. Plan pending migrations
    pending = manager.plan()
    assert len(pending) == 2
    assert pending[0].version == "001"
    
    # 2. Idempotent Dry-run (should not apply anything)
    dry_run_res = manager.apply(apply=False)
    assert len(dry_run_res) == 2
    assert dry_run_res[0]["dry_run"] is True
    
    # Check that database table t1 does not exist yet
    with sqlite3.connect(db_file) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='t1';")
        assert cursor.fetchone() is None
        
    # 3. Apply migrations
    applied_res = manager.apply(apply=True)
    assert len(applied_res) == 2
    assert applied_res[0]["dry_run"] is False
    
    # Check that t1 now exists
    with sqlite3.connect(db_file) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='t1';")
        assert cursor.fetchone() is not None
        
    # 4. Plan again (should be empty/idempotent)
    pending_after = manager.plan()
    assert len(pending_after) == 0
    
    # 5. Apply again (should return empty list)
    apply_after = manager.apply(apply=True)
    assert len(apply_after) == 0
