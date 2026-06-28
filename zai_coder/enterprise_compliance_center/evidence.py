"""Evidence collection and mapping."""

from __future__ import annotations

import json
from pathlib import Path, PurePosixPath
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
    normalized = path.replace("\\", "/").strip()
    candidate = PurePosixPath(normalized)
    if candidate.is_absolute() or ".." in candidate.parts:
        return False
    lowered_parts = {part.lower() for part in candidate.parts}
    if ".git" in lowered_parts or any("secret" in part or "credential" in part or part.startswith(".env") for part in lowered_parts):
        return False
    return normalized.startswith(SAFE_EVIDENCE_PATHS) or any(part.startswith("BUILD_REPORT") for part in candidate.parts)


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


def auto_discover_evidence(root=".") -> list[dict]:
    import os
    discovered = []
    
    # We will map known filenames to controls
    # Just a heuristic map for the sake of the upgrade
    filename_to_control = {
        "role_matrix": "cc-access-001",
        "tenant_isolation_policy": "cc-access-001",
        "access_review_log": "cc-access-001",
        "audit_log_sample": "cc-audit-001",
        "retention_policy": "cc-audit-001",
        "observability_dashboard": "iso-ops-001",
        "incident_report": "iso-ops-001",
        "postmortem": "iso-ops-001",
        "processing_register": "gdpr-data-001",
        "lawful_basis_register": "pdpa-consent-001",
        "privacy_notice": "pdpa-consent-001"
    }

    try:
        for dirpath, _, filenames in os.walk(root):
            if ".git" in dirpath or "__pycache__" in dirpath:
                continue
            for f in filenames:
                basename = f.split(".")[0]
                if basename in filename_to_control:
                    filepath = os.path.join(dirpath, f)
                    try:
                        item = map_evidence(
                            control_id=filename_to_control[basename],
                            title=basename,
                            source_path=filepath,
                            evidence_type="document"
                        )
                        discovered.append(item.to_dict())
                    except Exception:
                        pass
    except Exception:
        pass
    
    return discovered

def evidence_gap_report(controls: list[dict], evidence: list[dict], execute: bool = False, root: str = ".") -> dict:
    if execute:
        auto_ev = auto_discover_evidence(root)
        # Merge discovered evidence with passed evidence
        seen = {e.get("title") for e in evidence}
        for ev in auto_ev:
            if ev["title"] not in seen:
                evidence.append(ev)
                
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
