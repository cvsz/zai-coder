import pytest
from zai_coder.core.scheduler import LocalScheduler

def test_scheduler_add_and_list_jobs(tmp_path):
    db_path = tmp_path / "scheduler.db"
    sched = LocalScheduler(db_path)
    
    job_id = sched.add_job("nightly-build", "make build", "0 0 * * *")
    jobs = sched.list_jobs()
    
    assert len(jobs) == 1
    assert jobs[0].id == job_id
    assert jobs[0].name == "nightly-build"
    assert jobs[0].command == "make build"
    assert jobs[0].schedule == "0 0 * * *"
    assert jobs[0].enabled is False
    assert jobs[0].profile == "default"

def test_scheduler_enable_disable(tmp_path):
    db_path = tmp_path / "scheduler.db"
    sched = LocalScheduler(db_path)
    job_id = sched.add_job("test-job", "echo test", "* * * * *")
    
    assert sched.list_jobs()[0].enabled is False
    
    sched.set_enabled(job_id, True)
    assert sched.list_jobs()[0].enabled is True
    
    sched.set_enabled(job_id, False)
    assert sched.list_jobs()[0].enabled is False

def test_scheduler_run_dry_run(tmp_path):
    db_path = tmp_path / "scheduler.db"
    sched = LocalScheduler(db_path)
    job_id = sched.add_job("safe-job", "make test", "0 * * * *")
    
    result = sched.run_job_dry_run(job_id)
    assert result["dry_run"] is True
    assert result["command"] == "make test"
    assert "Would execute command: make test" in result["message"]

def test_scheduler_delete_job(tmp_path):
    db_path = tmp_path / "scheduler.db"
    sched = LocalScheduler(db_path)
    job_id = sched.add_job("to-delete", "echo", "* * * * *")
    assert len(sched.list_jobs()) == 1
    
    sched.delete_job(job_id)
    assert len(sched.list_jobs()) == 0
