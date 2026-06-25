"""Incident report generator."""

from __future__ import annotations

from dataclasses import dataclass, field

from .models import now_iso


@dataclass(frozen=True)
class IncidentReport:
    title: str
    severity: str
    summary: str
    affected_systems: tuple[str, ...] = ()
    timeline: tuple[str, ...] = ()
    actions: tuple[str, ...] = ()
    created_at: str = field(default_factory=now_iso)

    def validate(self) -> list[str]:
        issues = []
        if not self.title:
            issues.append("title required")
        if self.severity not in {"sev1", "sev2", "sev3", "sev4"}:
            issues.append("severity must be sev1..sev4")
        if not self.summary:
            issues.append("summary required")
        return issues

    def to_markdown(self) -> str:
        timeline = "\n".join(f"- {item}" for item in self.timeline) or "- pending"
        systems = "\n".join(f"- {item}" for item in self.affected_systems) or "- pending"
        actions = "\n".join(f"- {item}" for item in self.actions) or "- pending"
        return f"""# Incident Report: {self.title}

Severity: {self.severity}
Created: {self.created_at}

## Summary

{self.summary}

## Affected systems

{systems}

## Timeline

{timeline}

## Actions

{actions}

## Follow-up

- Capture logs.
- Review execution journal.
- Review provider audit.
- Confirm rollback or recovery.
"""


def incident_report_template(title: str = "Service degradation", severity: str = "sev3") -> IncidentReport:
    return IncidentReport(
        title=title,
        severity=severity,
        summary="Describe what happened, current impact, and current mitigation.",
        affected_systems=("api", "execution-runner"),
        timeline=("detection time pending", "mitigation time pending"),
        actions=("run healthcheck", "review alerts", "generate recovery plan"),
    )
