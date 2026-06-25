"""Document templates."""

from __future__ import annotations

from .models import DocumentProject, DocumentSection


def technical_spec_template(title: str) -> DocumentProject:
    return DocumentProject(
        title=title,
        audience="engineering",
        purpose="technical specification",
        sections=[
            DocumentSection("Summary", "Describe the problem and target outcome."),
            DocumentSection("Requirements", "- Functional requirements\n- Non-functional requirements"),
            DocumentSection("Architecture", "Describe modules, data flow, and integration points."),
            DocumentSection("Safety", "Document guardrails, permissions, and rollback plan."),
            DocumentSection("Test Plan", "List validation commands and acceptance criteria."),
        ],
    )


def runbook_template(title: str) -> DocumentProject:
    return DocumentProject(
        title=title,
        audience="operators",
        purpose="operational runbook",
        sections=[
            DocumentSection("Purpose", "Explain what this runbook covers."),
            DocumentSection("Preflight", "List checks before running operations."),
            DocumentSection("Procedure", "Step-by-step commands."),
            DocumentSection("Rollback", "How to safely recover."),
            DocumentSection("Verification", "How to confirm success."),
        ],
    )
