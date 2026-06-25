from __future__ import annotations

import json
import time
from pathlib import Path

from zai_coder.tui.actions import list_palette_commands
from zai_coder.tui.config import load_tui_config
from zai_coder.tui.loader import load_template, normalize_template_name, template_entries
from zai_coder.tui.messages import HELP_TEXT, TEXTUAL_MISSING_MESSAGE
from zai_coder.tui.persistence import load_persisted_state, save_persisted_state
from zai_coder.tui.state import TuiState


def run_tui(template_name: str | None = None, dry_run: bool = False, no_textual: bool = False, root: str | Path | None = None) -> int:
    project_root = Path(root or ".").resolve()
    config = load_tui_config(project_root)
    template_key = normalize_template_name(template_name or config.get("template", "command-center"))
    state = _load_state(project_root, config)
    state.active_template = template_key
    state.workspace = str(project_root)
    state.add_log(f"Selected template: {template_key}")

    if dry_run:
        template = load_template(template_key, state=state)
        print(json.dumps(_launch_plan(config, template.as_dict(), project_root), indent=2))
        _save_state(project_root, config, state)
        return 0

    if no_textual:
        template = load_template(template_key, state=state)
        print(template.render_static())
        _save_state(project_root, config, state)
        return 0

    return _launch_textual(template_key, state, config, project_root)


def _load_state(project_root: Path, config: dict) -> TuiState:
    if config.get("persist_state", True):
        return load_persisted_state(project_root, config.get("state_path", ".zai-coder/tui-state.json"))
    return TuiState()


def _save_state(project_root: Path, config: dict, state: TuiState) -> None:
    if config.get("persist_state", True):
        save_persisted_state(project_root, config.get("state_path", ".zai-coder/tui-state.json"), state)


def _launch_plan(config: dict, template: dict, project_root: Path) -> dict:
    return {
        "mode": "dry-run",
        "project": "zai-coder",
        "root": str(project_root),
        "template": template,
        "dry_run_first": config.get("dry_run_first", True),
        "refresh_interval_seconds": config.get("refresh_interval_seconds", 1),
        "textual_required_for_real_launch": True,
        "allowed_local_actions": [
            "./run.sh doctor",
            "make safety-check",
            "make final-release-status",
            "make install-dry-run",
            "./run.sh tui --print-config",
        ],
        "blocked_by_default": [
            "git push",
            "gh release",
            "terraform apply",
            "kubectl apply",
            "docker push",
            "cloudflare",
            "stripe",
            "APPLY=1",
            "secret-bearing commands",
        ],
    }


def _launch_textual(template_key: str, state: TuiState, config: dict, project_root: Path) -> int:
    try:
        from textual.app import App, ComposeResult
        from textual.containers import Horizontal, Vertical
        from textual.widgets import Footer, Header, Input, Static
    except ImportError:
        print(TEXTUAL_MISSING_MESSAGE, end="")
        return 1

    class ZaiCoderTuiApp(App):
        CSS = """
        Screen {
            background: #061017;
            color: #d8fff7;
        }
        #main {
            height: 1fr;
        }
        .panel {
            border: round #2b5465;
            background: #0d1b24;
            padding: 1 2;
            margin: 1;
        }
        #work {
            width: 2fr;
        }
        #side {
            width: 1fr;
        }
        #command {
            dock: bottom;
            margin: 0 1 1 1;
            border: round #77d7c8;
        }
        """
        BINDINGS = [
            ("q", "quit", "Quit"),
            ("ctrl+k", "command_palette", "Command Palette"),
            ("ctrl+r", "refresh", "Refresh"),
            ("ctrl+d", "toggle_dry_run", "Toggle Dry Run"),
            ("f1", "help", "Help"),
            ("ctrl+a", "approve_dry_run", "Approve Dry Run"),
        ]

        def __init__(self, tui_state: TuiState, tui_config: dict) -> None:
            super().__init__()
            self.tui_state = tui_state
            self.tui_config = tui_config

        def compose(self) -> ComposeResult:
            yield Header(show_clock=True)
            with Horizontal(id="main"):
                yield Static(self._render_template(), id="work", classes="panel")
                with Vertical(id="side", classes="panel"):
                    yield Static(self._render_status(), id="status")
                    yield Static(self._render_palette(), id="palette")
            yield Input(placeholder="Type a local note or use ctrl+k for commands", id="command")
            yield Footer()

        def on_mount(self) -> None:
            self.set_interval(self.tui_config.get("refresh_interval_seconds", 1), self._tick)

        def _tick(self) -> None:
            self.tui_state.refresh_timestamp = time.time()
            self.query_one("#status", Static).update(self._render_status())

        def _render_template(self) -> str:
            template = load_template(self.tui_state.active_template, state=self.tui_state)
            return template.render_static()

        def _render_status(self) -> str:
            return "\n".join(
                [
                    f"workspace: {self.tui_state.workspace}",
                    f"dry-run: {'on' if self.tui_state.dry_run_mode else 'off'}",
                    f"session: {self.tui_state.current_session}",
                    f"template: {self.tui_state.active_template}",
                    f"last command: {self.tui_state.last_command or 'none'}",
                ]
            )

        def _render_palette(self) -> str:
            items = "\n".join(f"- {item}" for item in list_palette_commands())
            return "Command Palette\n" + items

        def action_refresh(self) -> None:
            self.tui_state.add_log("Manual refresh")
            self.query_one("#work", Static).update(self._render_template())
            self.query_one("#status", Static).update(self._render_status())

        def action_toggle_dry_run(self) -> None:
            self.tui_state.dry_run_mode = not self.tui_state.dry_run_mode
            self.tui_state.add_log(f"Dry-run mode set to {self.tui_state.dry_run_mode}")
            self.action_refresh()

        def action_command_palette(self) -> None:
            self.tui_state.last_focus = "command-palette"
            self.query_one("#palette", Static).update(self._render_palette() + "\n\nPalette focused.")

        def action_help(self) -> None:
            self.query_one("#work", Static).update(HELP_TEXT)

        def action_approve_dry_run(self) -> None:
            self.tui_state.add_log("Dry-run evidence approved locally; apply remains blocked by default.")
            self.query_one("#status", Static).update(self._render_status())

        def action_quit(self) -> None:
            _save_state(project_root, config, self.tui_state)
            self.exit()

    app = ZaiCoderTuiApp(state, config)
    app.run()
    _save_state(project_root, config, state)
    return 0


def describe_templates() -> str:
    return "\n".join(f"{entry['route_id']} {entry['name']} - {entry['purpose']}" for entry in template_entries())
