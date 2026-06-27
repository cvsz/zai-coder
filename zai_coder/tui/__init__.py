"""Optional Textual TUI template system for ZAI Coder.

The package is safe to import without Textual installed. Real TUI launch imports
Textual lazily inside ``zai_coder.tui.app``.
"""

from .loader import list_templates, load_template, normalize_template_name
from .task_panel import TaskPanelAdapter
from .state import TuiState

__all__ = ["TuiState", "TaskPanelAdapter", "list_templates", "load_template", "normalize_template_name"]
