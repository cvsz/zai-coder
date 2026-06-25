from zai_coder.tui.loader import load_template
from zai_coder.tui.state import TuiState


def test_templates_render_production_static_previews():
    state = TuiState(active_template="command-center")
    for name in (
        "command-center",
        "agent-hub",
        "flow-stream",
        "architect-tree",
        "creative-canvas",
        "operation-gate",
    ):
        state.active_template = name
        rendered = load_template(name, state=state).render_static()
        assert "ZAI Coder TUI" in rendered
        assert "Command Palette" in rendered
        assert name in rendered


def test_operation_gate_contains_required_gate_labels():
    rendered = load_template("operation-gate").render_static()
    for label in ("Plan", "Dry Run", "Review", "Approval", "Apply", "Verify", "Rollback"):
        assert label in rendered
