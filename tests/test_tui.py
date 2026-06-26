from zai_coder.tui.integrations import TuiIntegrations
from zai_coder.tui.loader import instantiate_template
from zai_coder.tui.state import TuiState

def test_tui_integrations(tmp_path):
    integ = TuiIntegrations(tmp_path)
    assert "Task DB" in integ.get_task_queue_list() or "tasks" in integ.get_task_queue_list() or "No tasks" in integ.get_task_queue_list()
    assert integ.get_local_server_status() in ["Online (port 8765)", "Offline"]
    assert "planner" in integ.get_agent_registry()
    assert "docs" in integ.get_skill_registry()
    assert "developer" in integ.get_policy_profile()
    assert integ.get_audit_tail()
    assert "DRY-RUN" in integ.get_safe_command_runner_dry_run()
    assert "PENDING" in integ.get_final_release_status()

def test_template_instantiation():
    state = TuiState()
    template = instantiate_template("command-center", state)
    assert template.name == "command-center"
    rendered = template.render_static()
    assert "zai-coder" in rendered
    assert "task_queue" not in rendered # Should be resolved
