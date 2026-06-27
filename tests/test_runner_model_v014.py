import pytest
from zai_coder.core.runner import AgentRunner

def test_runner_model_creation(tmp_path):
    runner = AgentRunner(tmp_path)
    run = runner.create_run("Fix bug X", "coder", parent_run_id="run-0")
    
    assert run.task == "Fix bug X"
    assert run.agent_name == "coder"
    assert run.status == "pending"
    assert run.parent_run_id == "run-0"
    assert str(tmp_path) in run.workspace
    
    d = run.to_dict()
    assert d["status"] == "pending"

def test_runner_dry_run_execution(tmp_path):
    runner = AgentRunner(tmp_path)
    run = runner.create_run("Check logs", "reviewer")
    
    result = runner.execute_dry_run(run)
    assert result.status == "completed"
    assert "DRY-RUN" in result.summary
    assert result.completed_at is not None
