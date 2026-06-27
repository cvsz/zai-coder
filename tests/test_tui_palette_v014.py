import pytest
from zai_coder.tui.app import create_tui_app
from zai_coder.tui.state import TuiState
from zai_coder.tui.config import TuiConfig
from zai_coder.tui.palette import CommandPalette

@pytest.mark.asyncio
async def test_tui_palette_open_and_select():
    config = TuiConfig()
    state = TuiState()
    # create_tui_app returns the app class
    AppClass = create_tui_app(config, state)
    app = AppClass(state, config)
    
    async with app.run_test() as pilot:
        # Manually trigger action to test screen push
        pilot.app.action_command_palette()
        await pilot.pause() # Allow screen push to process
        
        assert isinstance(pilot.app.screen, CommandPalette)
        
        # Select action
        await pilot.press("down")
        await pilot.press("enter")
        
        # Verify action result
        assert any("Palette selected" in log for log in state.log_buffer)
