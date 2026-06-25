"""Postmortem generator."""

from __future__ import annotations

from pathlib import Path


def postmortem_markdown(incident: dict, healing_plan: dict | None = None) -> str:
    plan = healing_plan or {}
    actions = "\n".join(f"- {action}" for action in plan.get("actions", [])) or "- No remediation actions executed."
    return f"""# Postmortem — {incident['title']}

## Incident

- ID: {incident['id']}
- Service: {incident['service']}
- Severity: {incident['severity']}
- Status: {incident['status']}

## Signals

{chr(10).join(f"- {s.get('metric')}: {s.get('value')} ({s.get('status')})" for s in incident.get('signals', [])) or "- No signals recorded."}

## Remediation Plan

{actions}

## Safety Review

- Auto-apply disabled.
- Rollback required.
- Approval required for high-risk remediation.
- Audit log required.

## Follow-up

- Add tests for the detected failure mode.
- Tune alert thresholds.
- Confirm rollback readiness.
"""


def write_postmortem(incident: dict, healing_plan: dict | None = None, root: str | Path = ".", out_dir: str = "incidents/reports") -> str:
    root = Path(root)
    path = root / out_dir / f"{incident['id']}-postmortem.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(postmortem_markdown(incident, healing_plan), encoding="utf-8")
    return str(path)
