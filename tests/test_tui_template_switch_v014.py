import pytest
from zai_coder.tui.app import create_tui_app
from zai_coder.tui.state import TuiState
from zai_coder.tui.config import TuiConfig

@pytest.mark.asyncio
async def test_tui_template_switch():
    config = TuiConfig()
    state = TuiState()
    AppClass = create_tui_app(config, state)
    app = AppClass(state, config)
    
    async with app.run_test() as pilot:
        initial_template = state.active_template
        pilot.app.action_switch_template("agent-hub")
        assert state.active_template == "agent-hub"
        assert state.active_template != initial_template
        assert any("agent-hub" in log for log in state.log_buffer)
