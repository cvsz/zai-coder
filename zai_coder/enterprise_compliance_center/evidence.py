"""Evidence collection and mapping."""

from __future__ import annotations

import json
from pathlib import Path
import uuid

from .models import EvidenceItem
from .controls import find_control


SAFE_EVIDENCE_PATHS = (
    "docs/",
    "assets/",
    "BUILD_REPORT",
    "compliance/",
    "incidents/reports/",
    "updates/manifests/",
)


def evidence_path_allowed(path: str) -> bool:
    normalized = path.replace("\\", "/")
    if any(part in normalized for part in [".env", "credentials", "secret", ".git/"]):
        return False
    return normalized.startswith(SAFE_EVIDENCE_PATHS) or "BUILD_REPORT" in normalized


def map_evidence(control_id: str, title: str, source_path: str, evidence_type: str = "document") -> EvidenceItem:
    if not evidence_path_allowed(source_path):
        raise ValueError("unsafe evidence path")
    control = find_control(control_id)
    item = EvidenceItem(
        id=f"ev_{uuid.uuid4().hex[:12]}",
        control_id=control.id,
        title=title,
        source_path=source_path,
        evidence_type=evidence_type,
    )
    issues = item.validate()
    if issues:
        raise ValueError("; ".join(issues))
    return item


def evidence_gap_report(controls: list[dict], evidence: list[dict]) -> dict:
    evidence_by_control = {}
    for item in evidence:
        evidence_by_control.setdefault(item["control_id"], []).append(item)
    gaps = []
    for control in controls:
        found_titles = {item["title"] for item in evidence_by_control.get(control["id"], [])}
        missing = [req for req in control.get("evidence_required", []) if req not in found_titles]
        if missing:
            gaps.append({"control_id": control["id"], "missing": missing})
    return {"ok": not gaps, "gaps": gaps, "evidence_count": len(evidence)}


def write_evidence_inventory(evidence: list[dict], root: str | Path = ".", out: str = "compliance/evidence/evidence-inventory.json") -> str:
    root = Path(root)
    path = root / out
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"evidence": evidence}, indent=2, sort_keys=True), encoding="utf-8")
    return str(path)
