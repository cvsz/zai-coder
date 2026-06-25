"""Game export adapter helpers."""

from __future__ import annotations

from zai_coder.creative_automation.export_adapters import phaser_export_plan, godot_export_plan, ExportPlan
from .models import GameProject


def export_game_project(project: GameProject, adapter: str = "phaser") -> ExportPlan:
    if adapter == "phaser":
        return phaser_export_plan(project.slug, project.title)
    if adapter == "godot":
        return godot_export_plan(project.slug, project.title)
    raise ValueError(f"unsupported game adapter: {adapter}")
