from __future__ import annotations

from dataclasses import dataclass

from .loader import list_templates, normalize_template_name


@dataclass
class TemplateNavigator:
    active_template: str = "command-center"

    def switch(self, template_name: str) -> str:
        normalized = normalize_template_name(template_name)
        if normalized not in list_templates():
            available = ", ".join(list_templates())
            raise ValueError(f"Cannot switch to unknown template '{template_name}'. Available: {available}")
        self.active_template = normalized
        return self.active_template

    def next_template(self) -> str:
        templates = list_templates()
        index = templates.index(self.active_template) if self.active_template in templates else 0
        self.active_template = templates[(index + 1) % len(templates)]
        return self.active_template
