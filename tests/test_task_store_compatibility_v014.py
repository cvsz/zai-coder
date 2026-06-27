from zai_coder.core.task_store import TaskStore


def test_task_store_legacy_and_self_queue_apis_coexist(tmp_path):
    store = TaskStore(tmp_path / "tasks.db")

    legacy_id = store.create_task("legacy task", "planner", "legacy prompt")
    assert legacy_id == 1

    legacy_task = store.get_task(legacy_id)
    assert legacy_task is not None
    assert legacy_task["state"] == "queued"
    assert legacy_task["status"] == "queued"

    modern_task = store.create(
        title="modern task",
        agent="builder",
        description="modern prompt",
        metadata={"ignored": "placeholder"},
    )
    assert modern_task["id"] == 2
    assert modern_task["state"] == "queued"
    assert modern_task["status"] == "queued"
    assert modern_task["prompt"] == "modern prompt"

    store.update_status(modern_task["id"], "running")
    assert store.get_task(modern_task["id"])["state"] == "running"
    assert store.get_task(modern_task["id"])["status"] == "running"

    store.update_task_state(legacy_id, "failed", error="boom")
    failed_task = store.get_task(legacy_id)
    assert failed_task["state"] == "failed"
    assert failed_task["status"] == "failed"
    assert failed_task["error"] == "boom"

    store.add_event(legacy_id, "start", "legacy start")
    store.append_event(modern_task["id"], "start", "modern start")
    assert store.get_events(legacy_id)[0]["message"] == "legacy start"
    assert store.get_events(modern_task["id"])[0]["message"] == "modern start"

    store.add_output(legacy_id, "assistant", "legacy output")
    store.append_output(modern_task["id"], "assistant", "modern output")
    assert store.get_outputs(legacy_id)[0]["content"] == "legacy output"
    assert store.get_outputs(modern_task["id"])[0]["content"] == "modern output"

    listed = store.list_tasks()
    assert {task["id"] for task in listed} == {legacy_id, modern_task["id"]}
    assert all("state" in task and "status" in task for task in listed)
