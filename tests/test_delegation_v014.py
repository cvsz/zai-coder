import pytest
from zai_coder.core.delegation import DelegationOrchestrator, SubagentConfig, DelegationPlan

def test_plan_delegation_validation(tmp_path):
    orch = DelegationOrchestrator(tmp_path)
    
    # Valid plan
    tasks = [
        {"agent_name": "coder", "task": "write code"},
        {"agent_name": "reviewer", "task": "review code"}
    ]
    plan = orch.plan_delegation("implement feature", tasks)
    assert len(plan.subagents) == 2
    assert plan.subagents[0].isolated_context is True
    assert plan.subagents[0].shared_state is False
    
    # Invalid plan: too many subagents
    tasks = [{"agent_name": "a", "task": "t"}] * 4
    with pytest.raises(ValueError, match="Exceeded max subagents"):
        orch.plan_delegation("big task", tasks)

    # Invalid plan: shared state
    plan = DelegationPlan("task", [SubagentConfig("coder", "code", shared_state=True)])
    with pytest.raises(ValueError, match="Shared mutable state is not allowed"):
        plan.validate()

def test_execute_plan_dry_run(tmp_path):
    orch = DelegationOrchestrator(tmp_path)
    tasks = [{"agent_name": "coder", "task": "write code"}]
    plan = orch.plan_delegation("implement feature", tasks)
    
    results = orch.execute_plan_dry_run(plan, parent_run_id="run-0")
    assert len(results) == 1
    assert results[0].agent_name == "coder"
    assert results[0].status == "completed"
    assert "[REDACTED_FOR_PARENT]" in results[0].summary
