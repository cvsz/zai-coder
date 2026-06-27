from zai_coder.tui.palette import PaletteController, PaletteEntry, default_palette_entries


def test_default_palette_contains_commands_and_template_switches():
    commands = [entry.command for entry in default_palette_entries()]
    assert "doctor" in commands
    assert "repo-check" in commands
    assert "switch operation-gate" in commands


def test_palette_opens_filters_and_selects_command():
    palette = PaletteController.create()
    palette.open()
    palette.set_query("repo")

    visible = palette.filtered_entries()

    assert visible
    assert visible[0].command == "repo-check"
    assert palette.selected_command() == "repo-check"
    assert "> Repo Check [repo-check]" in palette.render()


def test_palette_navigation_wraps():
    palette = PaletteController(
        [
            PaletteEntry("help", "Help"),
            PaletteEntry("refresh", "Refresh"),
        ]
    )
    palette.open()

    assert palette.selected_command() == "help"
    assert palette.move_previous().command == "refresh"
    assert palette.move_next().command == "help"


def test_palette_search_typing_and_backspace():
    palette = PaletteController.create()
    palette.open()
    palette.append_query("s")
    palette.append_query("a")
    assert palette.query == "sa"
    palette.backspace()
    assert palette.query == "s"


def test_palette_runs_selected_command():
    palette = PaletteController.create()
    palette.open()
    palette.set_query("compile")
    executed: list[str] = []

    palette.run_selected(executed.append)

    assert executed == ["compile"]


def test_palette_escape_style_close_clears_focus_state():
    palette = PaletteController.create()
    palette.open("doctor")
    palette.close()

    assert palette.is_open is False
    assert palette.query == ""
    assert palette.selected_index == 0
