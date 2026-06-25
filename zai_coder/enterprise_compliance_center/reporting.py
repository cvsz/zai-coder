"""Compliance reports."""

from __future__ import annotations

from pathlib import Path

from .frameworks import framework_catalog
from .controls import control_library
from .data_register import retention_summary
from .risk_matrix import risk_control_matrix


def compliance_report_markdown() -> str:
    frameworks = framework_catalog()
    controls = control_library()
    risks = risk_control_matrix()
    return f"""# Enterprise Compliance Center Report

## Frameworks

{chr(10).join(f"- {f['id']}: {f['name']} {f['version']}" for f in frameworks)}

## Controls

{chr(10).join(f"- {c['id']}: {c['title']} ({c['status']})" for c in controls)}

## Retention Summary

- Max retention days: {retention_summary()['max_retention_days']}
- PII records: {len(retention_summary()['pii_records'])}

## Risks

{chr(10).join(f"- {r['risk_id']}: {r['level']} score={r['score']} controls={','.join(r['controls'])}" for r in risks)}

## Safety

- This is a readiness report, not a certification.
- Evidence with secrets is excluded.
- Legal hold and retention gates block unsafe deletion.
"""


def write_compliance_report(root: str | Path = ".", out: str = "compliance/reports/compliance-readiness-report.md") -> str:
    root = Path(root)
    path = root / out
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(compliance_report_markdown(), encoding="utf-8")
    return str(path)
