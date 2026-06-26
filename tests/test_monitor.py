from zai_coder.core.monitor import SystemMonitor

def test_system_monitor_methods(tmp_path):
    monitor = SystemMonitor(tmp_path)
    
    disk = monitor.get_disk_usage()
    assert "total_gb" in disk
    assert "used_gb" in disk
    
    # create dummy db for checking
    db_dir = tmp_path / ".zai-coder" / "tasks"
    db_dir.mkdir(parents=True, exist_ok=True)
    db_path = db_dir / "tasks.db"
    db_path.write_text("dummy")
    
    assert monitor.check_db_health(db_path)["status"] == "error"
    assert monitor.check_db_health(tmp_path / "missing.db")["status"] == "missing"
    
    # check snapshot
    snap = monitor.get_snapshot()
    assert "python_version" in snap
    assert "platform" in snap
    assert snap["task_db"]["status"] == "error"
