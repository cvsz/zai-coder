from zai_coder.tui.output import OutputPanel


def test_output_panel_updates_buffer():
    panel = OutputPanel(id="output")
    panel.update_output("Command finished")

    assert panel.last_output == "Command finished"
