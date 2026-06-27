from __future__ import annotations

import json
import time
from pathlib import Path

from zai_coder.tui.actions import list_palette_commands
from zai_coder.tui.command_router import TuiCommandDecision, route_tui_command
from zai_coder.tui.config import TuiConfig, load_tui_config
from zai_coder.tui.loader import instantiate_template, normalize_template_name, template_entries
from zai_coder.tui.messages import TEXTUAL_MISSING_MESSAGE
from zai_coder.tui.output import format_action_result, format_output_panel
from zai_coder.tui.persistence import load_persisted_state, save_persisted_state
from zai_coder.tui.screens import render_about_screen, render_config_screen, render_help_screen, render_templates_screen
from zai_coder.tui.state import TuiState, switch_template

COMMAND_INPUT_ID = "command"


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
            "make repo-check",
            "make secret-scan",
            "make final-release-status",
            "make install-dry-run",
            "python3 -m pytest -q",
            "python3 -m compileall -q zai_coder",
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


def submit_tui_command(
    command_str: str,
    state: TuiState,
    config: TuiConfig,
    project_root: str | Path | None = None,
) -> TuiCommandDecision:
    project_path = Path(project_root or state.workspace or ".").resolve()
    state.record_command(command_str)
    decision = route_tui_command(command_str)

    if decision.blocked:
        message = f"BLOCKED: {decision.command}\nreason: {decision.reason}"
        state.add_log(message)
        state.add_output(message)
        return decision

    if not decision.allowed:
        message = f"UNKNOWN: {decision.command or command_str}\nreason: {decision.reason}"
        state.add_log(message)
        state.add_output(message)
        return decision

    command_key = decision.command.split(maxsplit=1)[0].lower()
    state.add_log(f"Command submitted: {decision.command}")

    if decision.kind == "switch":
        switch_template(state, decision.target)
        state.add_output(f"Switched template to {decision.target}")
        return decision

    if decision.kind == "action":
        from zai_coder.tui.actions import run_safe_action

        result = run_safe_action(decision.command, dry_run=True, cwd=project_path)
        state.add_output(format_action_result(result))
        return decision

    if command_key == "help":
        state.add_output(render_help_screen())
    elif command_key == "refresh":
        state.refresh_timestamp = time.time()
        state.add_output("Status sidebar refreshed.")
    elif command_key == "palette":
        state.last_focus = "command-palette"
        state.add_output("Command Palette\n" + "\n".join(f"- {item}" for item in list_palette_commands()))
    elif command_key == "config":
        state.add_output(render_config_screen(config))
    elif command_key == "about":
        state.add_output(render_about_screen())
    elif command_key == "dry-run":
        state.dry_run_mode = not state.dry_run_mode
        mode = "on" if state.dry_run_mode else "off"
        state.add_output(f"Dry-run mode set to {mode}. TUI shell commands are still planned through the safety router.")
    elif command_key == "templates":
        state.add_output(render_templates_screen())
    elif command_key == "quit":
        state.add_output("Quit requested.")
    else:  # pragma: no cover - defensive guard for future builtins
        state.add_output(f"Command accepted: {decision.command}")
    return decision


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
        #output {
            height: 13;
            border: round #77d7c8;
            background: #07151d;
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
                with Vertical(id="work", classes="panel"):
                    yield Static(self._render_template(), id="template")
                    yield Static(self._render_output(), id="output")
                with Vertical(id="side", classes="panel"):
                    yield Static(self._render_status(), id="status")
                    yield Static(self._render_palette(), id="palette")
            yield Input(placeholder="Type help, doctor, repo-check, switch agent-hub...", id=COMMAND_INPUT_ID)
            yield Footer()

        def on_mount(self) -> None:
            self.set_interval(self.tui_config.get("refresh_interval_seconds", 1), self._tick)
            self.query_one(f"#{COMMAND_INPUT_ID}", Input).focus()

        def on_input_submitted(self, event: Input.Submitted) -> None:
            decision = submit_tui_command(event.value, self.tui_state, self.tui_config, project_root)
            event.input.value = ""
            self._refresh_panels()
            if decision.allowed and decision.command.split(maxsplit=1)[0].lower() == "quit":
                self.action_quit()

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
                    f"outputs: {len(self.tui_state.output_buffer)}",
                ]
            )

        def _render_palette(self) -> str:
            items = "\n".join(f"- {item}" for item in list_palette_commands())
            return "Command Palette\n" + items

        def _render_output(self) -> str:
            return format_output_panel(self.tui_state.output_buffer)

        def _refresh_panels(self) -> None:
            self.query_one("#template", Static).update(self._render_template())
            self.query_one("#status", Static).update(self._render_status())
            self.query_one("#palette", Static).update(self._render_palette())
            self.query_one("#output", Static).update(self._render_output())

        def action_refresh(self) -> None:
            submit_tui_command("refresh", self.tui_state, self.tui_config, project_root)
            self._refresh_panels()

        def action_toggle_dry_run(self) -> None:
            submit_tui_command("dry-run", self.tui_state, self.tui_config, project_root)
            self._refresh_panels()

        def action_command_palette(self) -> None:
            submit_tui_command("palette", self.tui_state, self.tui_config, project_root)
            self._refresh_panels()

        def action_help(self) -> None:
            submit_tui_command("help", self.tui_state, self.tui_config, project_root)
            self._refresh_panels()

        def action_approve_dry_run(self) -> None:
            self.tui_state.add_log("Dry-run evidence approved locally; apply remains blocked by default.")
            self._refresh_panels()

        def action_quit(self) -> None:
            _save_state(project_root, config, self.tui_state)
            self.exit()

    return ZaiCoderTuiApp


def describe_templates() -> str:
    return "\n".join(f"{entry['route_id']} {entry['name']} - {entry['purpose']}" for entry in template_entries())
