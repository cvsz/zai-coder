from zai_coder.tui.loader import instantiate_template, normalize_template_name

class TemplateController:
    def __init__(self, state):
        self.state = state

    def switch_template(self, template_name: str) -> None:
        normalized = normalize_template_name(template_name)
        self.state.active_template = normalized
        self.state.add_log(f"Switched template to: {normalized}")
