from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .config import TuiConfig
from .loader import normalize_template_name, template_names
from .persistence import save_persisted_state
from .state import TuiState, switch_template


@dataclass
class TemplateSwitchResult:
    template: str
    persisted: bool
    message: str


@dataclass
class TemplateController:
    state: TuiState
    config: TuiConfig
    root: str | Path

    def switch(self, template_name: str, *, persist: bool = True) -> TemplateSwitchResult:
        normalized = normalize_template_name(template_name)
        if normalized not in template_names():
            available = ", ".join(template_names())
            raise ValueError(f"Unknown template '{template_name}'. Available templates: {available}")

        switch_template(self.state, normalized)
        persisted = False
        if persist and self.config.persist_state:
            persisted = save_persisted_state(self.root, self.config.state_path, self.state)

        status = "persisted" if persisted else "not persisted"
        return TemplateSwitchResult(
            template=normalized,
            persisted=persisted,
            message=f"Switched template to {normalized} ({status}).",
        )


def switch_active_template(
    state: TuiState,
    config: TuiConfig,
    root: str | Path,
    template_name: str,
    *,
    persist: bool = True,
) -> TemplateSwitchResult:
    return TemplateController(state=state, config=config, root=root).switch(template_name, persist=persist)
