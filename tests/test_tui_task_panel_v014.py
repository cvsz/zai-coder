from __future__ import annotations

from zai_coder.core.task_store import TaskStore
from zai_coder.tui.integrations import TuiIntegrations
from zai_coder.tui.task_panel import TaskPanelAdapter


def test_task_panel_adapter_renders_read_only_summary(tmp_path):
    adapter = TaskPanelAdapter(tmp_path)
    assert adapter.render() == "Task DB not initialized."

    store = TaskStore(tmp_path / ".zai-coder" / "tasks" / "tasks.db")
    task_id = store.create_task("review diff", "reviewer", "inspect diff")
    store.update_task_state(task_id, "running")

    rendered = adapter.render()
    assert "Tasks:" in rendered
    assert "RUNNING" in rendered
    assert "review diff" in rendered


def test_tui_integrations_use_task_panel_adapter(tmp_path):
    store = TaskStore(tmp_path / ".zai-coder" / "tasks" / "tasks.db")
    store.create_task("queue item", "planner", "inspect repo")

    integ = TuiIntegrations(tmp_path)
    summary = integ.get_task_queue_list()

    assert "queued" in summary.lower()
    assert "done" in summary.lower()

