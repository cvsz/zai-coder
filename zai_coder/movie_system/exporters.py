"""Movie export adapter helpers."""

from __future__ import annotations

from zai_coder.creative_automation.export_adapters import movie_export_plan, ExportPlan
from .models import MovieProject
from .screenplay import render_treatment


def export_movie_project(project: MovieProject) -> ExportPlan:
    return movie_export_plan(project.title, render_treatment(project))
