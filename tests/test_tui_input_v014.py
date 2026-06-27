import pytest
from zai_coder.tui.app import create_tui_app
from zai_coder.tui.state import TuiState
from zai_coder.tui.config import TuiConfig

@pytest.mark.asyncio
async def test_tui_input_focus_on_mount():
    config = TuiConfig()
    state = TuiState()
    # create_tui_app returns the app class
    AppClass = create_tui_app(config, state)
    app = AppClass(state, config)
    
    async with app.run_test() as pilot:
        assert pilot.app.focused.id == "command"

@pytest.mark.asyncio
async def test_tui_input_submit():
    config = TuiConfig()
    state = TuiState()
    AppClass = create_tui_app(config, state)
    app = AppClass(state, config)
    
    async with app.run_test() as pilot:
        input_widget = pilot.app.query_one("#command")
        input_widget.value = "help"
        await pilot.press("enter")
        
        assert input_widget.value == ""
        assert state.last_command == "help"
        # Verify log entry added to log_buffer
        assert any("help" in log for log in state.log_buffer)
