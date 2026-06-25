"""Board pack validation and safety gates."""

from __future__ import annotations


def board_pack_safety_gate(pack: dict, approval_id: str = "", external_publish_requested: bool = False) -> dict:
    blocked = []
    if not pack.get("dry_run", True):
        blocked.append("board pack must remain dry-run/export-only")
    if external_publish_requested:
        blocked.append("external publish is disabled by this package")
    if external_publish_requested and not approval_id.startswith("approved_"):
        blocked.append("external publish would require approval")

    # Only explicit positive flags are treated as prohibited claims. Disclaimers
    # such as "not audited financial statements" or risk warnings about
    # certification confusion must remain allowed.
    explicit_claims = {
        "certification_claim": bool(pack.get("certification_claim", False)),
        "audited_financial_claim": bool(pack.get("audited_financial_claim", False)),
        "external_publish": bool(pack.get("external_publish", False)),
    }
    if explicit_claims["certification_claim"] or explicit_claims["audited_financial_claim"]:
        blocked.append("pack must not claim certification or audited financial status")
    return {"allowed": not blocked, "blocked": blocked, "pack_id": pack.get("id"), "explicit_claims": explicit_claims}


def board_pack_quality_check(pack: dict) -> dict:
    checks = {
        "has_sections": bool(pack.get("sections")),
        "has_kpis": bool(pack.get("kpis")),
        "has_decisions": "decisions" in pack,
        "has_risks": "risks" in pack,
        "has_safety_notice": pack.get("dry_run", True) is True,
    }
    blocked = [key for key, ok in checks.items() if not ok]
    return {"ok": not blocked, "blocked": blocked, "checks": checks}
