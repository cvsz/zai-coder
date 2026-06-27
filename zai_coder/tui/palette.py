from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from .command_router import list_tui_commands


@dataclass(frozen=True)
class PaletteEntry:
    command: str
    label: str
    kind: str = "command"


def _label_for_command(command: str) -> str:
    if command.startswith("switch "):
        return "Switch: " + command.removeprefix("switch ").replace("-", " ").title()
    return command.replace("-", " ").title()


def default_palette_entries() -> list[PaletteEntry]:
    entries: list[PaletteEntry] = []
    seen: set[str] = set()
    for command in list_tui_commands():
        if command in seen:
            continue
        seen.add(command)
        kind = "template-switch" if command.startswith("switch ") else "command"
        entries.append(PaletteEntry(command=command, label=_label_for_command(command), kind=kind))
    return entries


@dataclass
class PaletteController:
    entries: list[PaletteEntry]
    is_open: bool = False
    query: str = ""
    selected_index: int = 0

    @classmethod
    def create(cls) -> "PaletteController":
        return cls(default_palette_entries())

    def open(self, query: str = "") -> None:
        self.is_open = True
        self.query = query
        self.selected_index = 0

    def close(self) -> None:
        self.is_open = False
        self.query = ""
        self.selected_index = 0

    def set_query(self, query: str) -> None:
        self.query = query
        self.selected_index = 0

    def append_query(self, character: str) -> None:
        if character and character.isprintable():
            self.set_query(self.query + character)

    def backspace(self) -> None:
        self.set_query(self.query[:-1])

    def filtered_entries(self) -> list[PaletteEntry]:
        needle = self.query.strip().lower()
        if not needle:
            return list(self.entries)
        return [
            entry
            for entry in self.entries
            if needle in entry.command.lower() or needle in entry.label.lower() or needle in entry.kind.lower()
        ]

    def move_next(self) -> PaletteEntry | None:
        return self._move(1)

    def move_previous(self) -> PaletteEntry | None:
        return self._move(-1)

    def selected_entry(self) -> PaletteEntry | None:
        visible = self.filtered_entries()
        if not visible:
            return None
        self.selected_index = max(0, min(self.selected_index, len(visible) - 1))
        return visible[self.selected_index]

    def selected_command(self) -> str | None:
        entry = self.selected_entry()
        return entry.command if entry else None

    def run_selected(self, runner: Callable[[str], object]) -> object | None:
        command = self.selected_command()
        if not command:
            return None
        return runner(command)

    def render(self) -> str:
        title = "Command Palette"
        suffix = f" search: {self.query}" if self.query else ""
        lines = [title + suffix]
        visible = self.filtered_entries()
        if not visible:
            lines.append("  no matches")
            return "\n".join(lines)
        self.selected_entry()
        for index, entry in enumerate(visible):
            marker = ">" if index == self.selected_index and self.is_open else "-"
            lines.append(f"{marker} {entry.label} [{entry.command}]")
        return "\n".join(lines)

    def _move(self, step: int) -> PaletteEntry | None:
        visible = self.filtered_entries()
        if not visible:
            self.selected_index = 0
            return None
        self.selected_index = (self.selected_index + step) % len(visible)
        return visible[self.selected_index]
