from __future__ import annotations

import json
import time
from pathlib import Path
from contextlib import asynccontextmanager

from zai_coder.tui.actions import list_palette_commands
from zai_coder.tui.command_router import TuiCommandRouter, route_tui_command
from zai_coder.tui.config import TuiConfig, load_tui_config
from zai_coder.tui.loader import instantiate_template, normalize_template_name, template_entries
from zai_coder.tui.navigation import command_palette_entries
from zai_coder.tui.messages import HELP_TEXT, TEXTUAL_MISSING_MESSAGE
from zai_coder.tui.output import OutputPanel
from zai_coder.tui.palette import CommandPalette
from zai_coder.tui.persistence import load_persisted_state, save_persisted_state
from zai_coder.tui.screens import HelpScreen
from zai_coder.tui.state import TuiState
from zai_coder.tui.template_controller import TemplateController


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

    return _launch_textual(state, config, project_root)


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


def _launch_textual(state: TuiState, config: TuiConfig, project_root: Path) -> int:
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
        class _Widget:
            def __init__(self, widget_id: str = "", value: str = "") -> None:
                self.id = widget_id
                self.value = value
                self.content = value

            def update(self, text: str) -> None:
                self.content = text

        class _Input(_Widget):
            pass

        class _OutputPanel(_Widget):
            def update_output(self, text: str) -> None:
                self.content = text

        class _Screen:
            pass

        class FallbackTuiApp:
            def __init__(self, tui_state: TuiState, tui_config: TuiConfig) -> None:
                self.tui_state = tui_state
                self.tui_config = tui_config
                self.template_controller = TemplateController(self.tui_state)
                self.router = TuiCommandRouter(self.tui_state)
                self.screen: object | None = None
                self.focused = _Input("command", "")
                self._palette_entries = command_palette_entries()
                self._palette_index = 0
                self._widgets = {
                    "command": self.focused,
                    "output": _OutputPanel("output", ""),
                    "work-panel": _Widget("work-panel", self._render_template()),
                    "status": _Widget("status", self._render_status()),
                    "palette": _Widget("palette", self._render_palette()),
                }
                self._setup_router()

            def _setup_router(self) -> None:
                self.router.register("help", lambda _: self.action_help())
                self.router.register("refresh", lambda _: self.action_refresh())
                self.router.register("palette", lambda _: self.action_command_palette())
                self.router.register("config", lambda _: self.action_config())
                self.router.register("about", lambda _: self.action_about())
                self.router.register("dry-run", lambda _: self.action_enable_dry_run())
                self.router.register("doctor", lambda _: self.action_local_command("doctor"))
                self.router.register("safety", lambda _: self.action_local_command("safety-check"))
                self.router.register("repo-check", lambda _: self.action_local_command("repo-check"))
                self.router.register("secret-scan", lambda _: self.action_local_command("secret-scan"))
                self.router.register("install-dry-run", lambda _: self.action_local_command("install-dry-run"))
                self.router.register("test", lambda _: self.action_local_command("test"))
                self.router.register("compile", lambda _: self.action_local_command("compile"))
                self.router.register("templates", lambda _: self.action_show_templates())
                self.router.register("quit", lambda _: self.action_quit())
                self.router.register("switch", lambda args: self.action_switch_template(args))

            def query_one(self, selector: str, cls=None):
                widget_id = selector.lstrip("#")
                if widget_id == "output" and isinstance(self._widgets["output"], _OutputPanel):
                    return self._widgets["output"]
                return self._widgets[widget_id]

            def push_screen(self, screen, callback=None):
                self.screen = screen
                self._palette_index = 0
                self._screen_callback = callback
                return screen

            def pop_screen(self):
                self.screen = None

            def exit(self):
                self.screen = None

            def run(self):
                return None

            @asynccontextmanager
            async def run_test(self):
                self.on_mount()

                class Pilot:
                    def __init__(self, app):
                        self.app = app

                    async def pause(self):
                        return None

                    async def press(self, key: str):
                        self.app._press(key)

                yield Pilot(self)

            def on_mount(self) -> None:
                self.focused = self._widgets["command"]
                self.action_refresh()

            def _press(self, key: str) -> None:
                if self.screen is not None and self._palette_entries:
                    if key == "down":
                        self._palette_index = min(self._palette_index + 1, len(self._palette_entries) - 1)
                        return
                    if key == "up":
                        self._palette_index = max(self._palette_index - 1, 0)
                        return
                    if key == "enter":
                        selection = self._palette_entries[self._palette_index].label
                        self.screen = None
                        callback = getattr(self, "_screen_callback", None)
                        if callback:
                            callback(selection)
                        return

                if key == "enter" and getattr(self.focused, "id", "") == "command":
                    event = type("Submitted", (), {"value": self.focused.value})()
                    self.on_input_submitted(event)

            def _render_command_result(self, command: str, decision, output) -> None:
                if command.startswith("switch "):
                    output.update_output(f"Switched template: {self.tui_state.active_template}")
                    return
                if decision.action is not None:
                    output.update_output(f"Allowlisted action: {decision.action.name}")
                    return
                if command in {"help", "config", "about", "palette", "refresh", "dry-run", "templates", "quit"}:
                    output.update_output(f"Executed: {command}")
                    return
                output.update_output(f"Handled: {command}")

            def on_input_submitted(self, event) -> None:
                command = event.value.strip()
                if not command:
                    return
                self.tui_state.last_command = command
                decision = route_tui_command(command)
                self.router.route(command)
                output = self.query_one("#output", _OutputPanel)
                if decision.status != "allowed":
                    self.tui_state.add_log(f"Submitted: {command}")
                    output.update_output(f"Unknown command: {command}")
                else:
                    self._render_command_result(command, decision, output)
                self.focused.value = ""
                self.action_refresh()

            def action_switch_template(self, template_name: str) -> None:
                template_name = template_name.strip()
                if not template_name:
                    return
                self.template_controller.switch_template(template_name)
                self.action_refresh()

            def action_enable_dry_run(self) -> None:
                self.tui_state.dry_run_mode = True
                self.tui_state.add_log("Dry-run mode enabled")
                self.action_refresh()

            def action_toggle_dry_run(self) -> None:
                self.tui_state.dry_run_mode = not self.tui_state.dry_run_mode
                self.tui_state.add_log(f"Dry-run mode set to {self.tui_state.dry_run_mode}")
                self.action_refresh()

            def action_local_command(self, command_name: str) -> None:
                self.tui_state.add_log(f"Allowlisted command selected: {command_name}")
                self.query_one("#output", _OutputPanel).update_output(
                    f"Dry-run only: {command_name} is allowlisted but execution stays blocked in this build."
                )

            def action_command_palette(self) -> None:
                self.tui_state.last_focus = "command-palette"
                self.push_screen(CommandPalette(), callback=self._on_palette_selected)

            def _on_palette_selected(self, selection: str | None) -> None:
                if not selection:
                    return
                self.tui_state.add_log(f"Palette selected: {selection}")
                if selection.startswith("Switch: "):
                    self.action_switch_template(selection.removeprefix("Switch: ").strip().lower().replace(" ", "-"))
                else:
                    self.query_one("#output", _OutputPanel).update_output(f"Palette selected: {selection}")
                self.action_refresh()

            def action_help(self) -> None:
                self.tui_state.add_log("Help requested")
                self.query_one("#work-panel", _Widget).update(HELP_TEXT)
                self.query_one("#output", _OutputPanel).update_output(HELP_TEXT)

            def action_show_templates(self) -> None:
                self.tui_state.add_log("Template list requested")
                self.query_one("#output", _OutputPanel).update_output(describe_templates())

            def action_config(self) -> None:
                config_json = json.dumps(self.tui_config.to_dict(), indent=2, sort_keys=True)
                self.tui_state.add_log("Config requested")
                self.query_one("#output", _OutputPanel).update_output(config_json)

            def action_about(self) -> None:
                about_text = "ZAI Coder local-first TUI command center"
                self.tui_state.add_log("About requested")
                self.query_one("#output", _OutputPanel).update_output(about_text)

            def action_refresh(self) -> None:
                self.tui_state.add_log("Manual refresh")
                self.query_one("#work-panel", _Widget).update(self._render_template())
                self.query_one("#status", _Widget).update(self._render_status())
                self.query_one("#palette", _Widget).update(self._render_palette())

            def action_approve_dry_run(self) -> None:
                self.tui_state.add_log("Dry-run evidence approved locally; apply remains blocked by default.")
                self.query_one("#status", _Widget).update(self._render_status())

            def action_quit(self) -> None:
                _save_state(project_root, config, self.tui_state)
                self.exit()

            def _tick(self) -> None:
                self.tui_state.refresh_timestamp = time.time()
                self.query_one("#status", _Widget).update(self._render_status())

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

        return FallbackTuiApp

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
            ("f1", "help_screen", "Help"),
            ("ctrl+a", "approve_dry_run", "Approve Dry Run"),
        ]

        def __init__(self, tui_state: TuiState, tui_config: TuiConfig) -> None:
            super().__init__()
            self.tui_state = tui_state
            self.tui_config = tui_config
            self.template_controller = TemplateController(self.tui_state)
            self.router = TuiCommandRouter(self.tui_state)
            self._setup_router()

        def _setup_router(self) -> None:
            self.router.register("help", lambda _: self.action_help())
            self.router.register("refresh", lambda _: self.action_refresh())
            self.router.register("palette", lambda _: self.action_command_palette())
            self.router.register("config", lambda _: self.action_config())
            self.router.register("about", lambda _: self.action_about())
            self.router.register("dry-run", lambda _: self.action_enable_dry_run())
            self.router.register("doctor", lambda _: self.action_local_command("doctor"))
            self.router.register("safety", lambda _: self.action_local_command("safety-check"))
            self.router.register("repo-check", lambda _: self.action_local_command("repo-check"))
            self.router.register("secret-scan", lambda _: self.action_local_command("secret-scan"))
            self.router.register("install-dry-run", lambda _: self.action_local_command("install-dry-run"))
            self.router.register("test", lambda _: self.action_local_command("test"))
            self.router.register("compile", lambda _: self.action_local_command("compile"))
            self.router.register("templates", lambda _: self.action_show_templates())
            self.router.register("quit", lambda _: self.action_quit())
            self.router.register("switch", lambda args: self.action_switch_template(args))

        def compose(self) -> ComposeResult:
            yield Header(show_clock=True)
            with Horizontal(id="main"):
                with Vertical(id="work"):
                    yield Static(self._render_template(), classes="panel", id="work-panel")
                    yield OutputPanel(id="output", classes="panel")
                with Vertical(id="side", classes="panel"):
                    yield Static(self._render_status(), id="status")
                    yield Static(self._render_palette(), id="palette")
            yield Input(placeholder="Type a local note or use ctrl+k for commands", id="command")
            yield Footer()

        def on_mount(self) -> None:
            self.query_one("#command", Input).focus()
            self.action_refresh()

        def on_input_submitted(self, event: Input.Submitted) -> None:
            command = event.value.strip()
            if not command:
                return

            self.tui_state.last_command = command
            decision = route_tui_command(command)
            self.router.route(command)
            output = self.query_one("#output", OutputPanel)

            if decision.status != "allowed":
                self.tui_state.add_log(f"Submitted: {command}")
                output.update_output(f"Unknown command: {command}")
            else:
                self._render_command_result(command, decision, output)

            self.query_one("#command", Input).value = ""
            self.action_refresh()

        def _render_command_result(self, command: str, decision, output: OutputPanel) -> None:
            if command.startswith("switch "):
                output.update_output(f"Switched template: {self.tui_state.active_template}")
                return

            if decision.action is not None:
                output.update_output(f"Allowlisted action: {decision.action.name}")
                return

            if command in {"help", "config", "about", "palette", "refresh", "dry-run", "templates", "quit"}:
                output.update_output(f"Executed: {command}")
                return

            output.update_output(f"Handled: {command}")

        def action_switch_template(self, template_name: str) -> None:
            template_name = template_name.strip()
            if not template_name:
                return
            self.template_controller.switch_template(template_name)
            self.action_refresh()

        def action_enable_dry_run(self) -> None:
            self.tui_state.dry_run_mode = True
            self.tui_state.add_log("Dry-run mode enabled")
            self.action_refresh()

        def action_toggle_dry_run(self) -> None:
            self.tui_state.dry_run_mode = not self.tui_state.dry_run_mode
            self.tui_state.add_log(f"Dry-run mode set to {self.tui_state.dry_run_mode}")
            self.action_refresh()

        def action_local_command(self, command_name: str) -> None:
            self.tui_state.add_log(f"Allowlisted command selected: {command_name}")
            self.query_one("#output", OutputPanel).update_output(
                f"Dry-run only: {command_name} is allowlisted but execution stays blocked in this build."
            )

        def action_command_palette(self) -> None:
            self.tui_state.last_focus = "command-palette"
            self.push_screen(CommandPalette(), callback=self._on_palette_selected)

        def _on_palette_selected(self, selection: str | None) -> None:
            if not selection:
                return

            self.tui_state.add_log(f"Palette selected: {selection}")
            if selection.startswith("Switch: "):
                self.action_switch_template(selection.removeprefix("Switch: ").strip().lower().replace(" ", "-"))
            else:
                self.query_one("#output", OutputPanel).update_output(f"Palette selected: {selection}")
            self.action_refresh()

        def action_help(self) -> None:
            self.tui_state.add_log("Help requested")
            self.query_one("#work-panel", Static).update(HELP_TEXT)
            self.query_one("#output", OutputPanel).update_output(HELP_TEXT)

        def action_show_templates(self) -> None:
            self.tui_state.add_log("Template list requested")
            self.query_one("#output", OutputPanel).update_output(describe_templates())

        def action_config(self) -> None:
            config_json = json.dumps(self.tui_config.to_dict(), indent=2, sort_keys=True)
            self.tui_state.add_log("Config requested")
            self.query_one("#output", OutputPanel).update_output(config_json)

        def action_about(self) -> None:
            about_text = "ZAI Coder local-first TUI command center"
            self.tui_state.add_log("About requested")
            self.query_one("#output", OutputPanel).update_output(about_text)

        def action_refresh(self) -> None:
            self.tui_state.add_log("Manual refresh")
            self.query_one("#work-panel", Static).update(self._render_template())
            self.query_one("#status", Static).update(self._render_status())
            self.query_one("#palette", Static).update(self._render_palette())

        def action_approve_dry_run(self) -> None:
            self.tui_state.add_log("Dry-run evidence approved locally; apply remains blocked by default.")
            self.query_one("#status", Static).update(self._render_status())

        def action_quit(self) -> None:
            _save_state(project_root, config, self.tui_state)
            self.exit()

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

    return ZaiCoderTuiApp


def describe_templates() -> str:
    return "\n".join(f"{entry['route_id']} {entry['name']} - {entry['purpose']}" for entry in template_entries())
