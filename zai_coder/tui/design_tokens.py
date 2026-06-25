from __future__ import annotations

from dataclasses import dataclass


THEME_NAME = "zeaz-glass-dark"


@dataclass(frozen=True)
class StatusChip:
    label: str
    value: str
    tone: str = "neutral"

    def render(self) -> str:
        return f"[{self.tone.upper()}] {self.label}: {self.value}"


ZEA_Z_COLORS = {
    "background": "#061017",
    "panel": "#0d1b24",
    "panel_alt": "#122836",
    "border_soft": "#2b5465",
    "border_bright": "#77d7c8",
    "text": "#d8fff7",
    "muted": "#7aa0a8",
    "accent": "#42e8c7",
    "warning": "#ffd166",
    "danger": "#ff5c7a",
    "success": "#6be675",
}

SPACING = {
    "panel_padding": 1,
    "panel_gap": 1,
    "status_chip_gap": 1,
}

BORDERS = {
    "soft": "rounded",
    "strong": "heavy",
    "inner": "solid",
}

STATUS_TONES = {
    "safe": "SAFE",
    "dry_run": "DRY-RUN",
    "ready": "READY",
    "warn": "WARN",
    "blocked": "BLOCKED",
    "active": "ACTIVE",
}


def render_chip(label: str, value: str, tone: str = "neutral") -> str:
    return StatusChip(label=label, value=value, tone=tone).render()


def render_token_summary() -> str:
    lines = [f"theme={THEME_NAME}", "terminal_native_glass=layered panels + soft borders + contrast"]
    lines.extend(f"{name}={value}" for name, value in ZEA_Z_COLORS.items())
    return "\n".join(lines)
