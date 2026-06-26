from __future__ import annotations

import json
import time
from pathlib import Path

from zai_coder.tui.actions import list_palette_commands
from zai_coder.tui.config import TuiConfig, load_tui_config
from zai_coder.tui.loader import instantiate_template, normalize_template_name, template_entries
from zai_coder.tui.messages import HELP_TEXT, TEXTUAL_MISSING_MESSAGE
from zai_coder.tui.persistence import load_persisted_state, save_persisted_state
from zai_coder.tui.state import TuiState


def run_tui(
    template_name: str | None = None,
    dry_run: bool = False,
    no_textual: bool = False,
    print_config: bool = False,
    list_templates: bool = False,
    root: str | Path | None = None,
) -> int:
    project_root = Path(root or ".").resolve()
    config = load_tui_config(root=project_root)
    if print_config:
        print(json.dumps(config.to_dict(), indent=2, sort_keys=True))
        return 0
    if list_templates:
        print(describe_templates())
        return 0
    template_key = normalize_template_name(template_name or config.template)
    state = _load_state(project_root, config)
    state.active_template = template_key
    state.workspace = str(project_root)
    state.add_log(f"Selected template: {template_key}")

    if dry_run:
        template = instantiate_template(template_key, state=state)
        print(json.dumps(_launch_plan(config, template.as_dict(), project_root), indent=2))
        _save_state(project_root, config, state)
        return 0

    if no_textual:
        template = instantiate_template(template_key, state=state)
        print(template.render_static())
        _save_state(project_root, config, state)
        return 0

    return _launch_textual(template_key, state, config, project_root)


def _load_state(project_root: Path, config: TuiConfig) -> TuiState:
    if config.persist_state:
        return load_persisted_state(project_root, config.state_path)
    return TuiState()


def _save_state(project_root: Path, config: TuiConfig, state: TuiState) -> None:
    if config.persist_state:
        save_persisted_state(project_root, config.state_path, state)


def _launch_plan(config: TuiConfig, template: dict, project_root: Path) -> dict:
    return {
        "mode": "dry-run",
        "project": "zai-coder",
        "root": str(project_root),
        "template": template,
        "dry_run_first": config.dry_run_first,
        "refresh_interval_seconds": config.refresh_interval_seconds,
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


def create_tui_app(config: TuiConfig, state: TuiState):
    return _create_textual_app(config, state, Path.cwd())


def _launch_textual(template_key: str, state: TuiState, config: TuiConfig, project_root: Path) -> int:
    app_class = _create_textual_app(config, state, project_root)
    if app_class is None:
        return 1
    app = app_class(state, config)
    app.run()
    _save_state(project_root, config, state)
    return 0


def _create_textual_app(config: TuiConfig, state: TuiState, project_root: Path):
    try:
        from textual.app import App, ComposeResult
        from textual.containers import Horizontal, Vertical
        from textual.widgets import Footer, Header, Input, Static
    except ImportError:
        print(TEXTUAL_MISSING_MESSAGE, end="")
        return None

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
            template = instantiate_template(self.tui_state.active_template, state=self.tui_state)
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

    return ZaiCoderTuiApp


def describe_templates() -> str:
    return "\n".join(f"{entry['route_id']} {entry['name']} - {entry['purpose']}" for entry in template_entries())
