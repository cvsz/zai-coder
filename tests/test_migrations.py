import pytest
from zai_coder.core.migrations import MigrationManager

def test_migration_manager(tmp_path):
    manager = MigrationManager(workspace=str(tmp_path))
    
    # initially status should have empty applied and pending = available
    status = manager.status()
    assert isinstance(status["applied"], list)
    assert isinstance(status["pending"], list)
    
    # apply with dry-run
    results = manager.apply(dry_run=True)
    for r in results:
        assert "[DRY RUN]" in r
        
    # apply for real
    results2 = manager.apply(dry_run=False)
    for r in results2:
        assert "[DRY RUN]" not in r
        
    # apply again should be idempotent (no pending)
    results3 = manager.apply(dry_run=False)
    assert len(results3) == 0
    
    # Check status again
    status_after = manager.status()
    assert len(status_after["pending"]) == 0
    assert len(status_after["applied"]) == len(status_after["available"])
