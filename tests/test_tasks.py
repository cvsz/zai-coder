from zai_coder.core.task_store import TaskStore
from zai_coder.core.task_runner import TaskRunner
from zai_coder.core.approvals import ActionApprover

def test_task_queue(tmp_path):
    db_path = tmp_path / "tasks.db"
    store = TaskStore(db_path)
    
    # test create
    task_id = store.create_task("test task", "planner", "test prompt")
    assert task_id == 1
    
    # test get
    t = store.get_task(task_id)
    assert t["state"] == "queued"
    assert t["title"] == "test task"
    
    # test list
    tasks = store.list_tasks()
    assert len(tasks) == 1
    assert tasks[0]["id"] == task_id
    
    # test run dry-run (cancelled)
    approver = ActionApprover(apply_mode=False)
    runner = TaskRunner(store, approver)
    runner.run(task_id)
    
    t = store.get_task(task_id)
    assert t["state"] == "cancelled"
    
    # test run apply (completed)
    task_id2 = store.create_task("test task 2", "planner", "test prompt")
    approver2 = ActionApprover(apply_mode=True)
    
    # mock prompt_for_approval to return True
    import zai_coder.core.approvals
    original_prompt = zai_coder.core.approvals.prompt_for_approval
    zai_coder.core.approvals.prompt_for_approval = lambda x: True
    try:
        runner2 = TaskRunner(store, approver2)
        runner2.run(task_id2)
        
        t2 = store.get_task(task_id2)
        assert t2["state"] == "completed"
    finally:
        zai_coder.core.approvals.prompt_for_approval = original_prompt
