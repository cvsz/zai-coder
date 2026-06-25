"""Document export adapter helpers."""

from __future__ import annotations

from zai_coder.creative_automation.export_adapters import document_export_plan, ExportPlan
from .models import DocumentProject
from .renderer import render_markdown


def export_document_project(project: DocumentProject) -> ExportPlan:
    return document_export_plan(project.title, render_markdown(project))
