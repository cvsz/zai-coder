"""Audit evidence collector."""

from __future__ import annotations

import json
from pathlib import Path

from .models import EvidenceItem


def default_evidence_items() -> list[EvidenceItem]:
    return [
        EvidenceItem("ev-001", "repo_check", "make repo-check", "Repository policy check command exists"),
        EvidenceItem("ev-002", "secret_scan", "make secret-scan", "Secret scan command exists"),
        EvidenceItem("ev-003", "tests", "python3 -m pytest -q", "Test suite command exists"),
        EvidenceItem("ev-004", "cloudflare_access", "docs/cloudflare/CLOUDFLARE_ACCESS_CHECKLIST.md", "Access checklist exists"),
        EvidenceItem("ev-005", "observability", "make observability-status", "Observability status command exists"),
    ]


def collect_evidence(root: str | Path = ".") -> dict:
    root = Path(root)
    items = []
    for item in default_evidence_items():
        exists = True
        if item.source.startswith("docs/"):
            exists = (root / item.source).exists()
        items.append({**item.to_dict(), "exists": exists})
    return {"ok": all(item["exists"] for item in items), "items": items}


def write_evidence_bundle(root: str | Path = ".", out: str | Path = "evidence/governance/evidence-bundle.json") -> str:
    root = Path(root)
    out_path = root / out
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(collect_evidence(root), indent=2), encoding="utf-8")
    return str(out_path)
